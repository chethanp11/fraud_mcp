# =============================================================== #
# ================== memory/short_term.py ======================= #
# --------------------------------------------------------------- #
# 📌 Purpose   : Store and retrieve recent memory for fast-access tasks
# 🧠 Storage   : In-memory cache backed by JSON file for persistence
# ✅ Used by   : memory_router.py
# =============================================================== #

import json
import os
from datetime import datetime
from . import memory_constants as mc

SHORT_TERM_FILE = os.path.join(os.path.dirname(__file__), "short_term.json")

# =============================================================== #
# ===================== SHORT-TERM MEMORY ======================= #
# =============================================================== #

def store_short_term(entry: dict):
    """
    Append an entry to the short-term memory JSON file.

    Args:
        entry (dict): The data to store. Must be JSON-serializable.
    """
    if not isinstance(entry, dict):
        raise ValueError("Entry must be a dictionary.")

    entry["timestamp"] = datetime.utcnow().isoformat()
    memory = retrieve_short_term()
    memory.append(entry)

    with open(SHORT_TERM_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def retrieve_short_term(filters: dict = None):
    """
    Retrieve short-term memory, optionally applying filters.

    Args:
        filters (dict): Key-value pairs to filter memory entries.

    Returns:
        list[dict]: Matching memory entries.
    """
    if not os.path.exists(SHORT_TERM_FILE):
        return []

    with open(SHORT_TERM_FILE, "r") as f:
        memory = json.load(f)

    if not filters:
        return memory

    return [item for item in memory if all(item.get(k) == v for k, v in filters.items())]

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #