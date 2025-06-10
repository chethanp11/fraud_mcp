# =============================================================== #
# ======================== utils/auth.py ======================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Basic token-based authentication and role checks
# 🔐 Usage     : Used in tools or agents that require gated access
# ✅ Used by   : planner, escalate tools, dashboards (optional)
# =============================================================== #

import os

# =============================================================== #
# =================== STATIC TOKEN & ROLE CONFIGS =============== #
# =============================================================== #
# In production, replace with dynamic DB or secrets manager lookup
AUTHORIZED_TOKENS = {
    "analyst-token": "fraud_analyst",
    "ops-token": "fraud_ops",
    "exec-token": "executive",
}

ROLE_HIERARCHY = {
    "fraud_analyst": 1,
    "fraud_ops": 2,
    "executive": 3,
}

# =============================================================== #
# ====================== AUTH CORE FUNCTION ===================== #
# =============================================================== #
def validate_token(token: str) -> str:
    """
    Validates the token and returns the corresponding role.

    Args:
        token (str): API token or session token

    Returns:
        str: Role string (e.g., "fraud_analyst")

    Raises:
        ValueError: If token is invalid
    """
    role = AUTHORIZED_TOKENS.get(token)
    if not role:
        raise ValueError("Invalid token provided.")
    return role

# =============================================================== #
# ===================== ROLE CHECK FUNCTION ===================== #
# =============================================================== #
def has_required_role(user_role: str, required_role: str) -> bool:
    """
    Checks if user role has sufficient privilege.

    Args:
        user_role (str): Role from token
        required_role (str): Role required to perform action

    Returns:
        bool: True if allowed, False otherwise
    """
    return ROLE_HIERARCHY.get(user_role, 0) >= ROLE_HIERARCHY.get(required_role, 0)

# =============================================================== #
# =================== SIMPLE COMPOSITE CHECK ==================== #
# =============================================================== #
def authorize(token: str, required_role: str) -> bool:
    """
    Composite function to validate token and role in one call.

    Args:
        token (str): API or session token
        required_role (str): Minimum required role

    Returns:
        bool: True if authorized

    Raises:
        ValueError: If token is invalid or role is insufficient
    """
    user_role = validate_token(token)
    if not has_required_role(user_role, required_role):
        raise ValueError("Insufficient role privileges.")
    return True

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #