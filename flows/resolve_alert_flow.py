# =============================================================== #
# ============== flows/resolve_alert_flow.py ==================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : LangGraph flow for resolving a fraud alert case
# 🎯 Flow     : fetch_logs → resolve_alert → notify_analyst
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

    # ========================================================= #
    # 📥 Step 1 – Fetch logs from last 'minutes'
    # ========================================================= #
    def step_fetch(state):
        minutes = state["input"].get("minutes", 60)
        logs = fetch_logs(minutes=minutes)
        return {"fetched_logs": logs}

    # ========================================================= #
    # 🛠 Step 2 – Resolve the alert using case log details
    # ========================================================= #
    def step_resolve(state):
        logs = state["fetched_logs"]
        resolution = resolve_alert(
            case_id=logs["case_id"],
            resolution_notes=logs.get("resolution_notes", "Auto-resolved"),
            resolved_by=logs.get("resolved_by", "fraud_mcp")
        )
        return {"resolution_result": resolution}

    # ========================================================= #
    # 📣 Step 3 – Notify analyst of resolution
    # ========================================================= #
    def step_notify(state):
        res = state["resolution_result"]
        result = notify_analyst(
            case_id=res["case_id"],
            account_id=res["account_id"],
            severity=res["severity"],
            summary=res.get("summary", "Alert resolved and logged.")
        )
        return {"notification_status": result.get("status", "sent")}

    # Graph Construction
    graph.add_node("fetch_logs", step_fetch)
    graph.add_node("resolve_alert", step_resolve)
    graph.add_node("notify_analyst", step_notify)

    graph.set_entry_point("fetch_logs")
    graph.add_edge("fetch_logs", "resolve_alert")
    graph.add_edge("resolve_alert", "notify_analyst")

    return graph.compile()