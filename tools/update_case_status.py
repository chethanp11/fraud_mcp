# =============================================================== #
# =============== tools/update_case_status.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Update status of a fraud case in the DB
# 🎯 Actions   : Patch case with new status & timestamp
# ✅ Used by  : flows/resolve_alert_flow.py
# =============================================================== #

import sqlite3
from datetime import datetime
from resources.db.fraud_cases_db import get_db_path

# =============================================================== #
# ======================= CASE STATUS UPDATER =================== #
# =============================================================== #
def update_case_status(case_id: str, new_status: str, notes: str = "") -> bool:
    """
    Updates the status and notes of an existing fraud case.

    Args:
        case_id (str): Unique ID of the case
        new_status (str): New status (e.g., resolved, under_review)
        notes (str): Optional notes or resolution summary

    Returns:
        bool: True if update successful, False otherwise
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        timestamp = datetime.utcnow().isoformat()
        cursor.execute("""
            UPDATE fraud_cases
            SET status = ?, notes = ?, updated_at = ?
            WHERE case_id = ?
        """, (new_status, notes, timestamp, case_id))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"[❌ ERROR] Failed to update case {case_id}: {e}")
        return False

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #