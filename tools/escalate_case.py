# =============================================================== #
# ==================== tools/escalate_case.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Escalate a flagged fraud case to compliance or supervisor
# 🎯 Sends    : Metadata with case ID, reasons, flags, severity, notes
# ✅ Used by  : detect_and_escalate_flow, decision_agent
# =============================================================== #

import datetime

# =============================================================== #
# ===================== ESCALATION FUNCTION ===================== #
# =============================================================== #
def escalate_case(case_id: str,
                  flags: list,
                  severity: str,
                  analyst_notes: str = "",
                  destination: str = "compliance") -> dict:
    """
    Simulates escalation of a fraud case.

    Args:
        case_id (str): Unique fraud case identifier
        flags (list): List of triggered rule names or ML signals
        severity (str): 'low' | 'medium' | 'high'
        analyst_notes (str): Optional notes from fraud analyst
        destination (str): Target destination ('compliance', 'supervisor')

    Returns:
        dict: Escalation payload with success confirmation
    """

    payload = {
        "case_id": case_id,
        "flags": flags,
        "severity": severity,
        "analyst_notes": analyst_notes,
        "destination": destination,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "status": "escalated"
    }

    # In a real system, send this to a queue or endpoint.
    print(f"[📣 Escalation Triggered] → {destination.upper()} | Case: {case_id}")
    print(f"Payload: {payload}")

    return payload

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #