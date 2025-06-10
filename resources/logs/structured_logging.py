# =============================================================== #
# =========== resources/logs/structured_logging.py ============== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Structured JSON logger for fraud MCP
# 🧾 Format    : Logs include timestamp, level, event, metadata
# ✅ Used by   : tools, agents, flows, health checks
# =============================================================== #

import json
import os
from datetime import datetime

# =============================================================== #
# ============== LOG FILE CONFIGURATION ========================= #
# =============================================================== #
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "fraud_mcp_log.jsonl")


# =============================================================== #
# =============== STRUCTURED LOGGING FUNCTION ================== #
# =============================================================== #
def log_event(level: str, event: str, metadata: dict = None):
    """
    Log a structured event to a JSON lines file.

    Args:
        level (str): Log level ("INFO", "WARNING", "ERROR", etc.)
        event (str): Short event description
        metadata (dict, optional): Additional contextual data
    """
    if metadata is None:
        metadata = {}

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level.upper(),
        "event": event,
        "metadata": metadata,
    }

    # Append as a JSON line
    with open(LOG_FILE_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


# =============================================================== #
# =================== COMMON SHORTCUT WRAPPERS ================= #
# =============================================================== #
def log_info(event: str, metadata: dict = None):
    log_event("INFO", event, metadata)

def log_warning(event: str, metadata: dict = None):
    log_event("WARNING", event, metadata)

def log_error(event: str, metadata: dict = None):
    log_event("ERROR", event, metadata)


# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #