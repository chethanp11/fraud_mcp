# =============================================================== #
# ================== agents/planner_agent.py ==================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Decide whether incoming transaction data should be
#               routed to a tool (e.g., detect_fraud) or a LangGraph flow
# 🎯 Returns   : Dict with 'type': ['tool', 'flow'], and 'name'
# ✅ Called by : Orchestrator or CLI interfaces
# =============================================================== #

import openai
import json
from prompts.planner_prompt import get_planner_prompt
from utils.auth import validate_intent

# =============================================================== #
# ======================== SETUP LLM ============================ #
# =============================================================== #
# 📌 In production, replace hardcoded key with os.getenv or config loader
openai.api_key = "sk-test"

# =============================================================== #
# ===================== PLANNER AGENT CORE ====================== #
# =============================================================== #

def plan_intent(transaction_data: dict) -> dict:
    """
    Uses LLM to classify the transaction data as intent for
    tool or flow execution (e.g., detect fraud, resolve alert).

    Args:
        transaction_data (dict): Transaction event or payload

    Returns:
        dict: {'type': 'tool' or 'flow', 'name': 'detect_fraud'}
    """

    # ------------------ Sanity / Risk Checks ------------------- #
    if not isinstance(transaction_data, dict):
        return {"type": "fallback", "name": "fallback_agent"}

    if not validate_intent(str(transaction_data)):
        return {"type": "fallback", "name": "fallback_agent"}

    # ---------------- Compose Prompt --------------------------- #
    planning_prompt = get_planner_prompt(transaction_data)

    # ---------------- Call LLM Planner ------------------------- #
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": planning_prompt}
            ],
            max_tokens=50,
            temperature=0
        )
        decision = response.choices[0].message["content"]
    except Exception as e:
        print("Planner agent LLM failed:", e)
        return {"type": "fallback", "name": "fallback_agent"}

    # ---------------- Parse Response --------------------------- #
    try:
        intent_type, name = decision.strip().lower().split(":")
        if intent_type in {"tool", "flow"}:
            return {"type": intent_type, "name": name}
    except Exception:
        pass

    # ---------------- Default Fallback ------------------------- #
    return {"type": "fallback", "name": "fallback_agent"}

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #