# =============================================================== #
# ================== tools/notify_analyst.py ==================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Notify fraud analyst of a new or updated case
# 🎯 Actions   : Logs notification or pushes to queue (MVP = log)
# ✅ Used by  : detect_fraud.py, escalate_case.py
# =============================================================== #

import datetime
from resources.logs.structured_logging import log_event

# =============================================================== #
# =================== FRAUD ANALYST NOTIFIER ==================== #
# =============================================================== #
def notify_analyst(case_id: str, account_id: str, severity: str, summary: str) -> None:
    """
    Logs or pushes a notification for analyst review.

    Args:
        case_id (str): Unique case ID
        account_id (str): Customer or account involved
        severity (str): Alert level - low, medium, high
        summary (str): Short description of issue
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    message = (
        f"[🔔 ALERT - {severity.upper()}] Case {case_id} on Account {account_id}: {summary}"
    )

    # Log it for MVP
    log_event("analyst_notification", {
        "case_id": case_id,
        "account_id": account_id,
        "severity": severity,
        "summary": summary,
        "timestamp": timestamp
    })

    print(message)

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #