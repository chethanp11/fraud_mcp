# =============================================================== #
# ================== agents/planner_agent.py ==================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Decide whether user intent should be routed to
#               a tool (e.g., detect_fraud) or a LangGraph flow
# 🎯 Returns  : Dict with 'type': ['tool', 'flow'], and 'name'
# ✅ Called by : Orchestrator or CLI interfaces
# =============================================================== #

from prompts.planner_prompt import get_planner_prompt
from utils.auth import validate_intent
import openai

# ------------------------- #
# Setup model (OpenAI) – can be replaced with client-agnostic later
# ------------------------- #
openai.api_key = "sk-test"  # Replace with env var in production

def plan_intent(user_message: str) -> dict:
    """
    Uses LLM to classify the user's message as a tool or flow intent.

    Args:
        user_message (str): Raw user input message

    Returns:
        dict: {'type': 'tool' or 'flow', 'name': 'resolve_alert' or 'detect_and_escalate_flow'}
    """

    # 🔐 Pre-check for dangerous intents
    if not validate_intent(user_message):
        return {"type": "fallback", "name": "fallback_agent"}

    # 🧠 Compose the planning prompt
    planning_prompt = get_planner_prompt(user_message)

    # 🎯 Send to LLM (OpenAI gpt-3.5-turbo or similar)
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": planning_prompt}],
            max_tokens=50,
            temperature=0
        )
        decision = response.choices[0].message["content"]
    except Exception as e:
        print("Planner agent failed:", e)
        return {"type": "fallback", "name": "fallback_agent"}

    # 🧩 Parse result (simple string format: tool:resolve_alert or flow:detect_and_escalate_flow)
    try:
        intent_type, name = decision.strip().lower().split(":")
        if intent_type in ["tool", "flow"]:
            return {"type": intent_type, "name": name}
    except Exception:
        pass

    # 🧯 Fallback if unable to classify
    return {"type": "fallback", "name": "fallback_agent"}