from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, NumberedListOutputParser , PydanticOutputParser
from .state import ComplianceState
from  src.models.schemas import ChunkCitation,RetrievedContext,ComplianceReport,ViolationFinding , ViolationFindingList
from pathlib import Path
from langchain_community.vectorstores import FAISS
import os 
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
import uuid
from datetime import datetime
load_dotenv()
PROMPTS_PATH = Path(os.getenv("PROMPTS_PATH"))
VECTORSTORE_PATH = Path(os.getenv("VECTORSTORE_PATH"))
EMBEDDINGS_MODEL = 'aminhaeri/risk-embed'
llm = ChatOllama(model='llama3',temperature=0,streaming= False)
    

with open(Path(PROMPTS_PATH) / 'prompts.txt') as file:
    template = file.read()
with open(Path(PROMPTS_PATH) / "retriever_compliance_prompt.txt") as file:
    reasoning_template = file.read()
with open(Path(PROMPTS_PATH) / 'violation_prompt.txt') as file:
    violation_listing_prompt = file.read()

def query_analyzer_node(state:ComplianceState) -> ComplianceState:
    print("STATE KEYS:", state.keys())
    document=state['input_document']
    doc_type = state['document_type']

    #op_parser = CommaSeparatedListOutputParser()
    op_parser = NumberedListOutputParser()
    prompt_text = PromptTemplate(
    template=template,
    input_variables=["document", "doc_type"],
    partial_variables={"format_instructions": op_parser.get_format_instructions()}
)
    chain = prompt_text| llm | op_parser
    questions = chain.invoke({'document':document,"doc_type":doc_type})
    #print(f"Generated {len(questions)} compliance questions")
    #print(state['compliance_questions'])
    
    return {"compliance_questions": questions}


def ChunkCitationWrapper(results) -> List[ChunkCitation]:
    citations = []
    for doc, score in results:
        citation = ChunkCitation(
            source=doc.metadata.get('source'),
            pg_no=doc.metadata.get('page_label', None),
            score=score,
            chunk_id=doc.metadata.get('id', None),
            chunk_text=doc.page_content
        )
        citations.append(citation)
    return citations

def rag_retriever_node(state: ComplianceState)-> dict:
    questions = state['compliance_questions']
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
    vectore_store = FAISS.load_local(VECTORSTORE_PATH,embeddings=embedding,allow_dangerous_deserialization=True)
    contexts=[]
    for question in questions:
        results = vectore_store.similarity_search_with_score(question,k=3)
        citation = ChunkCitationWrapper(results)
        context = RetrievedContext(question=question , associated_chks=citation)
        contexts.append(context)
   # print("#"*30 ,f"\nRetrieved Context for   {len(contexts)} \n\n " , "#"*30)
    return {'retrieved_contexts' : contexts}

def compliance_reasoning_node(state: ComplianceState) -> dict:
    document = state['input_document']
    contexts =  state['retrieved_contexts']
    reasoning_prompt_template = PromptTemplate(
        template = reasoning_template , input_variables=['document' , 'question' , 'chunks']
    )
    chain = reasoning_prompt_template | llm 
    full_trace = '' 

    for ctx in contexts:
        chunk_txt = "\n\n---\n\n".join(
            [f"Source: {c.source}\n{c.chunk_text}" for c in ctx.associated_chks]
        )
        response = chain.invoke({
            "document":document,
            "question": ctx.question,
            "chunks": chunk_txt,
            'doc_type':state["document_type"]
        })
        full_trace += f"\nQuestion: {ctx.question}\n{response.content}\n{'-'*50}\n"
    return {'reasoning_trace':full_trace}

def violation_node(state: ComplianceState) -> dict:
    reasoning_trace = state['reasoning_trace']
    parser = PydanticOutputParser(pydantic_object=ViolationFindingList)
    prompt = PromptTemplate(template=violation_listing_prompt , input_variables=['reasoning_trace'] , partial_variables={'format_instructions': parser.get_format_instructions()})
    chain = prompt | llm | parser

    result = chain.invoke({'reasoning_trace':reasoning_trace})
    severity_order = ['low','medium','high','critical']
    max_sev ='low'
    for finding in result.findings:
        if severity_order.index(finding.severity)>severity_order.index(max_sev):
            max_sev = finding.severity
   # print('-'*50, f"\n total findings {len(result.findings)} severity {max_sev}",'-'*50)
    return {
        'findings' : result.findings , 
        'max_severity' : max_sev
    }
def report_compiler_node(state:ComplianceState) ->dict:
    findings = state['findings']
    reasoning = state['reasoning_trace']
    severity = state['max_severity']
    report = f""" 
    Compliance Audit Report
        ## Overall Severity : {severity.upper()}
        ## Report_id : str{uuid.uuid4()}
        ## Generated_on : {datetime.now().strftime("%d %b, %Y  %H:%M")}"
        ## Findings:
             """
    for i ,f in enumerate(findings,1):
        report+= f""" 
                ### Finding {i}
                - Violation {f.violation}    
                - Severity {f.severity}
                - Reasoning {f.reasoning}
                - Confidence {f.confidence}
                """
    report += "\n ## Detailed Analysis\n" + reasoning
    return {
        "report_markdown":report
        , "escalated":False
    }

def human_escalation_node(state: ComplianceState) -> dict:
    findings = state['findings']
    severity = state['max_severity']
    
    report = f"""
# CRITICAL ESCALATION — Human Review Required
- **Severity:** {severity.upper()}
- **Total Violations:** {len(findings)}

## Violations Requiring Immediate Attention:
"""
    for i, f in enumerate(findings, 1):
        report += f"""
### Finding {i}
- **Violation:** {f.violation}
- **Severity:** {f.severity}
- **Reasoning:** {f.reasoning}
"""
    report += "\n**This report has been flagged for immediate human review.**"
    
    return {
        "report_markdown": report,
        "audit_id": str(uuid.uuid4()),
        "escalated": True
    }
    
#def 
if __name__ == "__main__":
    test_state = {
        "input_document": "Customer transferred $15,000 to an overseas account in three separate transactions of $5,000 each within 24 hours.",
        "document_type": "transaction",
        "compliance_questions": [],
        "retrieved_contexts": [],
        "reasoning_trace": "",
        "findings": [],
        "max_severity": "",
        "report_markdown": "",
        "audit_id": "",
        "escalated": False
    }
    
    result = query_analyzer_node(test_state)
    for q in result["compliance_questions"]:
        print(f"- {q}")

    state_after_node1 = {**test_state, **query_analyzer_node(test_state)}
    print('*'*50,"state 1 aok",'*'*50)
    result = rag_retriever_node(state_after_node1)

    for ctx in result["retrieved_contexts"]:
        print(f"\nQuestion: {ctx.question}")
        for cit in ctx.associated_chks:
            print(f"  Source: {cit.source} | Score: {cit.score:.4f}")
            print(f"  Text: {cit.chunk_text[:150]}")
    state_after_node2 = {**state_after_node1, **result}
    print('*'*50,"state2 aok",'*'*50)
    reasoning_result = compliance_reasoning_node(state_after_node2)
    print(reasoning_result['reasoning_trace'][:1000])
    print('*'*50,"state 2 a ok",'*'*50)
    state_after_node3 = {**state_after_node2, **reasoning_result}
    scoring_result = violation_node(state_after_node3)

    for f in scoring_result['findings']:
        print(f"Violation : {f.violation}")
        print(f"Severity : {f.severity}")
        print(f"Reasoning : {f.reasoning[:200]}")
    print(f"Max severity: {scoring_result['max_severity']}")
    print(f"Total findings: {len(scoring_result['findings'])}")  

    print("state 3 a Ok")      

    state_after_node4 = {**state_after_node3, **scoring_result}
