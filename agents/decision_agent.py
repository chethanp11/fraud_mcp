# =============================================================== #
# =============== agents/decision_agent.py ====================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Perform decision branching based on context,
#               memory, risk score, or grounded rules
# 🎯 Returns  : Refined tool/flow name or branch path
# ✅ Called by : Planner agent or LangGraph flow node
# =============================================================== #

from utils.compliance_checker import run_compliance_rules
from memory.memory_router import fetch_recent_context
from shared_libs.vector_store.qdrant_connector import query_vector_store

# -------------------------- #
# 💡 Decision Context Router
# -------------------------- #
def decide_next_step(task_context: dict) -> dict:
    """
    Make a branching decision based on input, memory, vector grounding, and rules.

    Args:
        task_context (dict): Includes user_msg, risk_score, recent_events, etc.

    Returns:
        dict: {'branch': 'high_risk_escalation', 'reason': 'Risk > 0.85'}
    """

    user_msg = task_context.get("user_msg", "")
    risk_score = float(task_context.get("risk_score", 0))
    user_id = task_context.get("user_id", "anonymous")

    # 🧠 Step 1: Fetch context memory
    memory = fetch_recent_context(user_id)

    # 📊 Step 2: Ground decision with Qdrant vector search
    grounding_results = query_vector_store(user_msg, top_k=2)

    # ✅ Step 3: Check compliance/fraud rules
    rule_flag, rule_reason = run_compliance_rules(user_msg, risk_score)

    # 🔀 Step 4: Decision logic
    if rule_flag:
        return {"branch": "escalate_to_compliance", "reason": rule_reason}

    if risk_score >= 0.85:
        return {"branch": "high_risk_escalation", "reason": "Risk score exceeds threshold"}

    if "known_pattern" in str(grounding_results).lower():
        return {"branch": "auto_resolve", "reason": "Matched known fraud pattern"}

    return {"branch": "manual_review", "reason": "Default path"}