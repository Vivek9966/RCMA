from typing import TypedDict , Annotated , List , Optional
import operator
from src.models.schemas import RetrievedContext , ViolationFinding


class ComplianceState(TypedDict):
    
    input_document: str
    document_type: str

    compliance_questions: Annotated[List[str], operator.add]
    retrieved_contexts: Annotated[List[str], operator.add]

    reasoning_trace: str

    findings: Annotated[List[ViolationFinding], operator.add]
    max_severity: str

    report_markdown: str
    audit_id: str
    escalated: bool