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
from typing import List, Dict, Optional

LONG_TERM_FILE = os.path.join(os.path.dirname(__file__), "long_term.json")

# =============================================================== #
# ======================= LONG-TERM MEMORY ====================== #
# =============================================================== #

def _ensure_file():
    if not os.path.exists(LONG_TERM_FILE):
        with open(LONG_TERM_FILE, "w") as f:
            json.dump([], f)


def store_long_term(record: Dict, append_only: bool = True):
    """
    Store a record in long-term memory for future learning and traceability.

    Args:
        record (dict): Must include context keys. Timestamp auto-added.
        append_only (bool): If False, can overwrite if record has unique ID.
    """
    if not isinstance(record, dict):
        raise ValueError("Record must be a dictionary.")

    record["timestamp"] = datetime.utcnow().isoformat()

    _ensure_file()
    memory = retrieve_long_term()

    if append_only:
        memory.append(record)
    else:
        # Overwrite if same id exists
        record_id = record.get("id")
        if record_id:
            memory = [r for r in memory if r.get("id") != record_id]
        memory.append(record)

    with open(LONG_TERM_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def retrieve_long_term(query_filter: Optional[Dict] = None) -> List[Dict]:
    """
    Retrieve long-term memory with optional filters.

    Args:
        query_filter (dict, optional): e.g., {"case_id": "C123"}

    Returns:
        list[dict]: Matching records
    """
    _ensure_file()

    with open(LONG_TERM_FILE, "r") as f:
        try:
            memory = json.load(f)
        except json.JSONDecodeError:
            memory = []

    if not query_filter:
        return memory

    return [
        entry for entry in memory
        if all(entry.get(k) == v for k, v in query_filter.items())
    ]


def clear_long_term():
    """
    Clear all long-term memory (dangerous — use for dev/testing only).
    """
    with open(LONG_TERM_FILE, "w") as f:
        json.dump([], f, indent=2)


def delete_record_by_key(key: str, value: str) -> bool:
    """
    Delete a record matching a specific key-value pair.

    Args:
        key (str): e.g., "case_id"
        value (str): e.g., "C123"

    Returns:
        bool: True if a record was deleted
    """
    memory = retrieve_long_term()
    updated_memory = [r for r in memory if r.get(key) != value]

    if len(updated_memory) == len(memory):
        return False

    with open(LONG_TERM_FILE, "w") as f:
        json.dump(updated_memory, f, indent=2)
    return True

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #