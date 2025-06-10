# =============================================================== #
# =============== agents/fallback_agent.py ====================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Handle unknown or unsupported instructions safely
# 🎯 Actions   : Clarify intent, log anomaly, or escalate gracefully
# ✅ Called by : Planner, Decision agent, or Orchestrator fallback
# =============================================================== #

from memory.memory_router import store_fallback_event
from utils.compliance_checker import is_compliant
from resources.logs.structured_logging import log_event

# =============================================================== #
# ======================= FALLBACK HANDLER ====================== #
# =============================================================== #

def handle_unknown_instruction(user_msg: str, user_id: str = "anonymous") -> dict:
    """
    Handles unclear or unsupported user instructions with intent clarification.

    Args:
        user_msg (str): Raw user input
        user_id (str): User/session ID

    Returns:
        dict: Fallback response with guidance
    """

    # 🧪 Input validation
    if not isinstance(user_msg, str):
        raise ValueError("user_msg must be a string")

    if not isinstance(user_id, str):
        user_id = "anonymous"

    # 🪵 Step 1: Log the fallback event
    try:
        log_event({
            "type": "fallback_triggered",
            "user_id": user_id,
            "message": user_msg
        })
    except Exception as e:
        print(f"[FallbackAgent] Logging failed: {e}")

    # 🧠 Step 2: Store in memory for future learning
    try:
        store_fallback_event(user_msg=user_msg, user_id=user_id)
    except Exception as e:
        print(f"[FallbackAgent] Memory store failed: {e}")

    # 🔒 Step 3: Check compliance policy
    try:
        if not is_compliant(user_msg):
            return {
                "response": "Your request could not be processed due to policy restrictions.",
                "action": "reject"
            }
    except Exception as e:
        print(f"[FallbackAgent] Compliance check failed: {e}")

    # 💬 Step 4: Generic fallback response
    return {
        "response": (
            "I'm not sure how to handle that instruction yet.\n\n"
            "Can you rephrase it or provide more detail?\n"
            "If this is urgent, please escalate manually or contact a human investigator."
        ),
        "action": "clarify"
    }

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #