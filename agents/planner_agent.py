# =============================================================== #
# ================== agents/planner_agent.py ==================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Decide whether incoming transaction data should be
#               routed to a tool (e.g., detect_fraud) or a LangGraph flow
# 🎯 Returns   : Dict with 'type': ['tool', 'flow'], and 'name'
# ✅ Called by : Orchestrator or CLI interfaces
# =============================================================== #

import openai
import os
import json
from prompts.planner_prompt import get_planner_prompt
from utils.auth import validate_intent

# =============================================================== #
# ======================== SETUP LLM ============================ #
# =============================================================== #
# 📌 Load from environment instead of hardcoding
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-test")  # Fallback for dev

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

    # =========================================================== #
    # 🧪 Validation
    # =========================================================== #
    if not isinstance(transaction_data, dict):
        raise ValueError("transaction_data must be a dictionary")

    # 🔐 Sanity check for malicious input
    if not validate_intent(str(transaction_data)):
        return {"type": "fallback", "name": "fallback_agent"}

    # =========================================================== #
    # 🧠 Compose Prompt from Transaction Payload
    # =========================================================== #
    planning_prompt = get_planner_prompt(transaction_data)

    # =========================================================== #
    # 🚀 Call LLM to classify intent
    # =========================================================== #
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
        print(f"[Planner Error] LLM failed: {e}")
        return {"type": "fallback", "name": "fallback_agent"}

    # =========================================================== #
    # 🧩 Parse and validate LLM output
    # =========================================================== #
    try:
        intent_type, name = decision.strip().lower().split(":")
        if intent_type in {"tool", "flow"}:
            return {"type": intent_type, "name": name}
    except Exception:
        print(f"[Planner Error] Could not parse decision: {decision}")

    # =========================================================== #
    # 🔁 Fallback for unhandled or unclear response
    # =========================================================== #
    return {"type": "fallback", "name": "fallback_agent"}

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #