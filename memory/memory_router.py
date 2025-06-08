# =============================================================== #
# ================= memory/memory_router.py ===================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Route memory operations between short-term and long-term
# 🔁 Handles   : Read/write based on duration, purpose, and context
# ✅ Used by  : agents, tools, and flows in fraud_mcp
# =============================================================== #

from .short_term import store_short_term, retrieve_short_term
from .long_term import store_long_term, retrieve_long_term

# =============================================================== #
# ====================== MEMORY ROUTER CORE ===================== #
# =============================================================== #

def store_memory(data: dict, scope: str = "short"):
    """
    Store memory based on scope.

    Args:
        data (dict): The memory payload to store.
        scope (str): "short" or "long"
    """
    if scope == "short":
        store_short_term(data)
    elif scope == "long":
        store_long_term(data)
    else:
        raise ValueError("Invalid memory scope. Use 'short' or 'long'.")

def retrieve_memory(scope: str = "short", filters: dict = None):
    """
    Retrieve memory based on scope and optional filters.

    Args:
        scope (str): "short" or "long"
        filters (dict): Optional dictionary to filter results

    Returns:
        list[dict]: Retrieved memory entries
    """
    if scope == "short":
        return retrieve_short_term(filters)
    elif scope == "long":
        return retrieve_long_term(filters)
    else:
        raise ValueError("Invalid memory scope. Use 'short' or 'long'.")

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #