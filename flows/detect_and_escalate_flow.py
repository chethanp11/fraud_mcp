# =============================================================== #
# ========= flows/detect_and_escalate_flow.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Sample LangGraph flow to detect fraud and escalate
# 🎯 Flow     : detect_fraud → escalate_case
# ✅ Used by  : flow_registry, orchestrator
# =============================================================== #

from langgraph.graph import StateGraph
from tools.detect_fraud import run as detect_fraud
from tools.escalate_case import run as escalate_case

# ----------------------------- #
# 📍 Flow State Definition
# ----------------------------- #
flow_state = {
    "input": dict,
    "fraud_detected": bool,
    "detection_result": dict,
    "escalation_result": dict,
}

# ----------------------------- #
# 🔁 LangGraph Flow Generator
# ----------------------------- #
def detect_and_escalate_flow():
    """
    Constructs a LangGraph flow:
    Step 1: Run fraud detection
    Step 2: If fraud detected → escalate case
    """

    graph = StateGraph(flow_state)

    # ========================================================= #
    # 🧪 Step 1 – Detect Fraud using input transaction data
    # ========================================================= #
    def step_detect(state):
        result = detect_fraud(transaction=state["input"])  # 🔧 Match tool signature
        return {
            "fraud_detected": result.get("fraud_detected", False),
            "detection_result": result,
        }

    # ========================================================= #
    # 🚨 Step 2 – Escalate only if fraud_detected is True
    # ========================================================= #
    def step_escalate(state):
        if not state.get("fraud_detected"):
            return {"escalation_result": None}

        det = state["detection_result"]
        return {
            "escalation_result": escalate_case(
                case_id=det["case_id"],
                flags=det["flags"],
                severity=det["severity"],
                analyst_notes=det.get("analyst_notes", ""),
                destination=det.get("destination", "compliance")
            )
        }

    # Build Graph
    graph.add_node("detect", step_detect)
    graph.add_node("escalate", step_escalate)

    graph.set_entry_point("detect")
    graph.add_edge("detect", "escalate")

    return graph.compile()