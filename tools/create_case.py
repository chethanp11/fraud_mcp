# =============================================================== #
# ====================== tools/create_case.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Create a new fraud case record in the database
# 🎯 Returns  : case_id and creation status
# ✅ Used by  : detect_fraud.py, resolve_alert.py
# =============================================================== #

import uuid
import datetime
from resources.db.fraud_cases_db import insert_case_record

# =============================================================== #
# ======================= CREATE CASE LOGIC ===================== #
# =============================================================== #
def create_case(account_id: str,
                description: str,
                severity: str,
                source: str,
                initial_flags: list) -> dict:
    """
    Creates a fraud case entry in the database.

    Args:
        account_id (str): ID of the potentially fraudulent account
        description (str): Brief case summary
        severity (str): 'low', 'medium', or 'high'
        source (str): Source system or detection trigger
        initial_flags (list): Detected fraud rules or ML triggers

    Returns:
        dict: Confirmation with case_id and status
    """
    case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
    created_at = datetime.datetime.utcnow().isoformat()

    case_data = {
        "case_id": case_id,
        "account_id": account_id,
        "description": description,
        "severity": severity,
        "source": source,
        "flags": initial_flags,
        "status": "open",
        "created_at": created_at
    }

    insert_case_record(case_data)

    print(f"[📂 New Fraud Case Opened] ID: {case_id}")
    return {"case_id": case_id, "status": "created"}

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #