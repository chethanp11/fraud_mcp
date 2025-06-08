# =============================================================== #
# =================== memory/long_term.py ======================= #
# --------------------------------------------------------------- #
# 📌 Purpose   : Persist long-term memory across fraud detection sessions
# 🧠 Storage   : JSON file for cumulative memory across flows & tools
# ✅ Used by   : memory_router.py, agents, tools, flows
# =============================================================== #

import json
import os
from datetime import datetime

LONG_TERM_FILE = os.path.join(os.path.dirname(__file__), "long_term.json")

# =============================================================== #
# ======================= LONG-TERM MEMORY ====================== #
# =============================================================== #

def store_long_term(record: dict):
    """
    Store a record in long-term memory for future learning and traceability.

    Args:
        record (dict): The memory record to store. Must include useful context.
    """
    if not isinstance(record, dict):
        raise ValueError("Record must be a dictionary.")

    record["timestamp"] = datetime.utcnow().isoformat()
    memory = retrieve_long_term()
    memory.append(record)

    with open(LONG_TERM_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def retrieve_long_term(query_filter: dict = None):
    """
    Retrieve stored long-term memory with optional filters.

    Args:
        query_filter (dict, optional): Dictionary of filters.

    Returns:
        list[dict]: Matching long-term records.
    """
    if not os.path.exists(LONG_TERM_FILE):
        return []

    with open(LONG_TERM_FILE, "r") as f:
        memory = json.load(f)

    if not query_filter:
        return memory

    return [entry for entry in memory if all(entry.get(k) == v for k, v in query_filter.items())]

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #