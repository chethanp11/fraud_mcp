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

# ----------------------------- #
# 🛑 Fallback Executor
# ----------------------------- #
def handle_unknown_instruction(user_msg: str, user_id: str = "anonymous") -> dict:
    """
    Handles unclear or unsupported user instructions with intent clarification.

    Args:
        user_msg (str): Raw user input
        user_id (str): User/session ID

    Returns:
        dict: Fallback response with guidance
    """

    # 1. Log the fallback event
    log_event({
        "type": "fallback_triggered",
        "user_id": user_id,
        "message": user_msg
    })

    # 2. Store for memory/retraining purposes
    store_fallback_event(user_msg=user_msg, user_id=user_id)

    # 3. Check if message violates policy
    if not is_compliant(user_msg):
        return {
            "response": "Your request could not be processed due to policy restrictions.",
            "action": "reject"
        }

    # 4. Default clarification response
    return {
        "response": (
            "I'm not sure how to handle that instruction yet.\n\n"
            "Can you rephrase it or provide more detail?\n"
            "If this is urgent, please escalate manually or contact a human investigator."
        ),
        "action": "clarify"
    }