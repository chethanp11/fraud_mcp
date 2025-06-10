# =============================================================== #
# ================== memory/short_term.py ======================= #
# --------------------------------------------------------------- #
# 📌 Purpose   : Manage short-term (session-level) memory storage
# 💾 Scope     : Volatile memory, cleared per session or flow reset
# 🎯 Used by   : Agents, tools, flows that need recent context
# =============================================================== #

import time
from typing import Any, Dict

# =============================================================== #
# ======================== SHORT TERM MEMORY ==================== #
# =============================================================== #

class ShortTermMemory:
    def __init__(self):
        """
        Initializes an empty short-term memory dictionary.
        """
        self._memory: Dict[str, Dict[str, Any]] = {}

    def set(self, session_id: str, key: str, value: Any) -> None:
        """
        Set a value in short-term memory for a given session.
        """
        if session_id not in self._memory:
            self._memory[session_id] = {}
        self._memory[session_id][key] = {
            "value": value,
            "timestamp": time.time()
        }

    def get(self, session_id: str, key: str) -> Any:
        """
        Get a value from short-term memory for a given session.
        """
        return self._memory.get(session_id, {}).get(key, {}).get("value")

    def get_all(self, session_id: str) -> Dict[str, Any]:
        """
        Retrieve all key-value pairs for a session.
        """
        return {
            k: v["value"] for k, v in self._memory.get(session_id, {}).items()
        }

    def clear(self, session_id: str) -> None:
        """
        Clear short-term memory for a given session.
        """
        self._memory.pop(session_id, None)

    def dump_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieve the full short-term memory (all sessions).
        """
        return {
            sid: {k: v["value"] for k, v in data.items()}
            for sid, data in self._memory.items()
        }

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #