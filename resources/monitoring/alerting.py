# =============================================================== #
# ============== resources/monitoring/alerting.py =============== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Send alerts when high-risk fraud cases are flagged
# 📢 Supports  : Logging-based alerts, email placeholders
# ✅ Used by   : tools/escalate_case.py, notify_analyst.py, fallback_agent.py
# =============================================================== #

import datetime
import logging
import os

ALERT_LOG = os.path.join(os.path.dirname(__file__), "..", "logs", "alerts.log")

# =============================================================== #
# ======================= ALERTING CORE ========================= #
# =============================================================== #

def send_alert(case_id: str, level: str, message: str, metadata: dict = None):
    """
    Sends an alert by logging it to a central alert file.

    Args:
        case_id (str): ID of the fraud case triggering the alert.
        level (str): Alert level - info, warning, error, critical.
        message (str): Summary of the alert.
        metadata (dict, optional): Additional context for traceability.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    alert_entry = {
        "timestamp": timestamp,
        "case_id": case_id,
        "level": level,
        "message": message,
        "metadata": metadata or {},
    }

    log_line = f"[{timestamp}] [{level.upper()}] Case: {case_id} | {message} | {metadata or '{}'}"
    os.makedirs(os.path.dirname(ALERT_LOG), exist_ok=True)

    with open(ALERT_LOG, "a") as f:
        f.write(log_line + "\n")

    if level.lower() in ["error", "critical"]:
        _trigger_email_placeholder(case_id, message)


def _trigger_email_placeholder(case_id, message):
    """
    Placeholder for future email/pager/webhook integration.
    """
    print(f"[ALERT EMAIL] 🚨 Case {case_id}: {message}")

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #