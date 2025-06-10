# =============================================================== #
# ================= flows/flow_registry.py ====================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Central registry for all LangGraph flows
# 🎯 Enables   : Dynamic selection and execution of flows
# ✅ Used by   : planner_agent, decision_agent, orchestrator
# =============================================================== #

from flows.detect_and_escalate_flow import detect_and_escalate_flow
from flows.resolve_alert_flow import resolve_alert_flow

# ----------------------------- #
# 📦 Flow Registry Dictionary
# ----------------------------- #
flow_registry = {
    "detect_and_escalate_flow": detect_and_escalate_flow,
    "resolve_alert_flow": resolve_alert_flow,
}

# ----------------------------- #
# 🔍 Flow Fetcher Function
# ----------------------------- #
def get_flow(flow_name: str):
    """
    Retrieves the corresponding LangGraph flow object based on name.

    Args:
        flow_name (str): Flow identifier (e.g., 'detect_and_escalate_flow')

    Returns:
        LangGraph flow function or None
    """
    return flow_registry.get(flow_name)