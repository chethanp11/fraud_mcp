# =============================================================== #
# ============== tools/resolve_alert.py ========================= #
# --------------------------------------------------------------- #
# 📌 Purpose   : Resolve an alert and update its case metadata
# 🎯 Updates   : Fraud case DB, logs resolution, notifies analyst
# ✅ Used by   : resolve_alert_flow, fraud_ops_ui
# =============================================================== #

from resources.db.fraud_cases_db import update_case_status_in_db
from tools.notify_analyst import send_notification
import json
from datetime import datetime

LOG_PATH = "resources/logs/fraud_events.log"

# =============================================================== #
# ======================== ALERT RESOLVER ======================= #
# =============================================================== #
def resolve_alert(case_id: str, resolution_notes: str, resolved_by: str):
    """
    Marks a fraud alert as resolved and updates system logs.

    Args:
        case_id (str): Unique ID of the case
        resolution_notes (str): Analyst remarks or findings
        resolved_by (str): Name or ID of the person resolving
    """
    status = update_case_status_in_db(case_id, new_status="resolved")

    if not status:
        raise Exception(f"[❌] Case {case_id} not found or update failed.")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "alert_resolved",
        "case_id": case_id,
        "resolved_by": resolved_by,
        "notes": resolution_notes,
    }

    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    send_notification(
        recipient=resolved_by,
        message=f"✅ Case {case_id} marked as resolved successfully."
    )

    return {"status": "success", "case_id": case_id}

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #