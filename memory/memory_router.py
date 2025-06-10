# =============================================================== #
# ================= memory/memory_router.py ===================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Route memory operations between short-term and long-term
# 🔁 Handles   : Read/write based on duration, purpose, and context
# ✅ Used by   : agents, tools, and flows in fraud_mcp
# =============================================================== #

from .short_term import store_short_term, retrieve_short_term
from .long_term import store_long_term, retrieve_long_term
from typing import Literal, Optional

# Supported memory scopes
MEMORY_SCOPES = {"short", "long"}

# =============================================================== #
# ====================== MEMORY ROUTER CORE ===================== #
# =============================================================== #

def store_memory(
    data: dict,
    scope: Literal["short", "long"] = "short",
    append_only: bool = True,
):
    """
    Route memory storage based on specified scope.

    Args:
        data (dict): The memory payload to store.
        scope (str): One of "short" or "long".
        append_only (bool): Only used for long-term memory.
    """
    if not isinstance(data, dict):
        raise TypeError("Memory data must be a dictionary.")

    if scope == "short":
        store_short_term(data)
    elif scope == "long":
        store_long_term(data, append_only=append_only)
    else:
        raise ValueError(f"Invalid memory scope '{scope}'. Choose from {MEMORY_SCOPES}.")


def retrieve_memory(
    scope: Literal["short", "long"] = "short",
    filters: Optional[dict] = None,
):
    """
    Retrieve memory from specified scope.

    Args:
        scope (str): One of "short" or "long".
        filters (dict, optional): Key-value filters for memory entries.

    Returns:
        list[dict]: Matching memory records.
    """
    if scope == "short":
        return retrieve_short_term(filters)
    elif scope == "long":
        return retrieve_long_term(filters)
    else:
        raise ValueError(f"Invalid memory scope '{scope}'. Choose from {MEMORY_SCOPES}.")

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #