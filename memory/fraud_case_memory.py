# =============================================================== #
# ================ memory/fraud_case_memory.py ================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Manage memory linked to specific fraud case IDs
# 🔁 Uses      : short_term + long_term for tracking case history
# ✅ Used by   : flows, tools, agents needing case-specific memory
# =============================================================== #

from .memory_router import store_memory, retrieve_memory
from typing import Optional, List

# =============================================================== #
# ==================== FRAUD CASE MEMORY API ==================== #
# =============================================================== #

def log_case_event(case_id: str, event: str, details: dict, scope: str = "short"):
    """
    Log an event or update for a given case.

    Args:
        case_id (str): Unique fraud case identifier.
        event (str): Label for the type of event (e.g., "escalated", "flagged").
        details (dict): Additional context for the event.
        scope (str): "short" or "long" memory.
    """
    memory_record = {
        "case_id": case_id,
        "event": event,
        "details": details
    }
    store_memory(memory_record, scope=scope)


def get_case_history(case_id: str, scope: str = "short") -> List[dict]:
    """
    Retrieve all memory events related to a case.

    Args:
        case_id (str): Case identifier.
        scope (str): "short" or "long".

    Returns:
        List[dict]: All memory events tied to the case ID.
    """
    filters = {"case_id": case_id}
    return retrieve_memory(scope=scope, filters=filters)


def get_recent_case_events(case_id: str, limit: int = 5) -> List[dict]:
    """
    Get the most recent events from both short- and long-term memory.

    Args:
        case_id (str): Case ID.
        limit (int): Max number of events to return.

    Returns:
        List[dict]: Ordered recent events across both memory types.
    """
    short = get_case_history(case_id, scope="short")
    long = get_case_history(case_id, scope="long")
    combined = sorted(short + long, key=lambda x: x.get("timestamp", ""), reverse=True)
    return combined[:limit]

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #