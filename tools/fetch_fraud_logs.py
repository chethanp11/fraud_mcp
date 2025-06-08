# =============================================================== #
# ============== tools/fetch_fraud_logs.py ====================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Fetch recent fraud logs for analysis/UI
# 🎯 Source    : Structured JSON logs from `resources/logs/`
# ✅ Used by   : fraud_ops_ui (log table), internal monitoring
# =============================================================== #

import os
import json
from datetime import datetime, timedelta

LOG_FILE_PATH = "resources/logs/fraud_events.log"

# =============================================================== #
# ======================= LOG FETCHER =========================== #
# =============================================================== #
def fetch_recent_logs(minutes: int = 60):
    """
    Fetches fraud logs from the past `minutes` duration.

    Args:
        minutes (int): Time window in minutes

    Returns:
        list[dict]: List of structured log entries
    """
    if not os.path.exists(LOG_FILE_PATH):
        return []

    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    recent_logs = []

    with open(LOG_FILE_PATH, "r") as f:
        for line in f:
            try:
                log = json.loads(line.strip())
                timestamp = datetime.fromisoformat(log.get("timestamp"))
                if timestamp >= cutoff_time:
                    recent_logs.append(log)
            except Exception as e:
                print(f"[⚠️ WARN] Skipping malformed log: {e}")

    return recent_logs

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #