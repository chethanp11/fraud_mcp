# =============================================================== #
# =================== config/constants.py ======================= #
# --------------------------------------------------------------- #
# 📌 Purpose   : Central store for global constants used across MCP
# 🔁 Constants : Risk levels, agent roles, status codes, etc.
# ✅ Used by  : fraud_mcp agents, tools, flows, and UI clients
# =============================================================== #

# =============================================================== #
# ======================= FRAUD CONSTANTS ======================= #
# =============================================================== #

RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
CASE_STATUSES = ["OPEN", "INVESTIGATING", "ESCALATED", "RESOLVED", "CLOSED"]
TRANSACTION_TYPES = ["WIRE", "ACH", "ATM", "P2P", "INTERNAL", "CHECK"]

# =============================================================== #
# ==================== AGENT & FLOW CONSTANTS =================== #
# =============================================================== #

AGENT_ROLES = {
    "PLANNER": "planner_agent",
    "DECISION": "decision_agent",
    "FALLBACK": "fallback_agent"
}

FLOW_NAMES = {
    "DETECT_AND_ESCALATE": "detect_and_escalate_flow",
    "RESOLVE_ALERT": "resolve_alert_flow"
}

# =============================================================== #
# ===================== COMPLIANCE FLAGS ======================== #
# =============================================================== #

COMPLIANCE_FLAGS = {
    "HIGH_VALUE_TXN": "Over threshold transfer",
    "SANCTION_HIT": "Party match on sanctions list",
    "LOCATION_MISMATCH": "Geo-IP vs known device mismatch"
}

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #