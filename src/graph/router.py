from src.graph.state import ComplianceState

def router(state: ComplianceState) -> str:
    severity = state['max_severity']

    if severity == 'critical':
        return 'human_escalation_node'
    else:
        return 'report_compiler_node'