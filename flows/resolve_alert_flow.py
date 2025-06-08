# =============================================================== #
# ============== flows/resolve_alert_flow.py ==================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : LangGraph flow for resolving a fraud alert case
# 🎯 Flow     : fetch_logs → analyze → resolve → notify_analyst
# ✅ Used by  : flow_registry, orchestrator
# =============================================================== #

from langgraph.graph import StateGraph
from tools.fetch_fraud_logs import run as fetch_logs
from tools.resolve_alert import run as resolve_alert
from tools.notify_analyst import run as notify_analyst

# ----------------------------- #
# 📍 Flow State Definition
# ----------------------------- #
flow_state = {
    "input": dict,
    "fetched_logs": dict,
    "resolution_result": dict,
    "notification_status": str,
}

# ----------------------------- #
# 🔁 LangGraph Flow Generator
# ----------------------------- #
def resolve_alert_flow():
    """
    Constructs LangGraph flow:
    Step 1: Fetch fraud logs
    Step 2: Resolve the fraud alert
    Step 3: Notify analyst
    """

    graph = StateGraph(flow_state)

    # Step 1 – Fetch logs
    def step_fetch(state):
        logs = fetch_logs(state["input"])
        return {"fetched_logs": logs}

    # Step 2 – Resolve alert
    def step_resolve(state):
        resolution = resolve_alert(state["fetched_logs"])
        return {"resolution_result": resolution}

    # Step 3 – Notify analyst
    def step_notify(state):
        result = notify_analyst(state["resolution_result"])
        return {"notification_status": result.get("status", "sent")}

    # Graph Construction
    graph.add_node("fetch_logs", step_fetch)
    graph.add_node("resolve_alert", step_resolve)
    graph.add_node("notify_analyst", step_notify)

    graph.set_entry_point("fetch_logs")
    graph.add_edge("fetch_logs", "resolve_alert")
    graph.add_edge("resolve_alert", "notify_analyst")

    return graph.compile()