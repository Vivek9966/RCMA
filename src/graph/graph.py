from langgraph.graph import StateGraph, END ,START
from .state  import ComplianceState
from .nodes import query_analyzer_node , rag_retriever_node ,compliance_reasoning_node , violation_node , report_compiler_node ,human_escalation_node
from .router import router

def graph():
    builder = StateGraph(ComplianceState)
    builder.add_node("query_analyzer_node",query_analyzer_node)
    builder.add_node('rag_retriever_node', rag_retriever_node)
    builder.add_node('compliance_reasoning_node',compliance_reasoning_node)
    builder.add_node('violation_node',violation_node)
    builder.add_node('report_compiler_node',report_compiler_node)
    builder.add_node('human_escalation_node',human_escalation_node)
    builder.set_entry_point('query_analyzer_node')
    builder.add_edge("query_analyzer_node", "rag_retriever_node")
    builder.add_edge("rag_retriever_node", "compliance_reasoning_node")
    builder.add_edge("compliance_reasoning_node", "violation_node")
    builder.add_conditional_edges(
        'violation_node',router,{
            "report_compiler_node":"report_compiler_node",
            "human_escalation_node":"human_escalation_node",
        }
    )

    builder.add_edge('report_compiler_node',END)
    builder.add_edge('human_escalation_node',END)

    graph = builder.compile()

    return graph

if __name__ == "__main__":
    test_graph = graph()
    result = test_graph.invoke({
        "input_document": "Customer transferred $15,000 to an overseas account in three separate transactions of $5,000 each within 24 hours.",
        "document_type": "transaction",
    })
    print(result["report_markdown"])
