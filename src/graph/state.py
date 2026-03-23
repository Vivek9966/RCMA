from typing import TypedDict , Annotated , List , Optional
import operator
from src.models.schemas import RetrievedContext , ViolationFinding


class ComplianceState(TypedDict):
    
    # user_input
    ip_doc : str
    doc_type: str

    # node1
    comp_ques : Annotated[List[str],operator.add]

    # node2
    retrive_context : Annotated[List[str],operator.add]

    #node3
    reasoning: str
    #node4
    findings : Annotated[List[ViolationFinding],operator.add]
    max_severity:str
    #node5
    report_md :str
    audit_id:str
    escalated : bool