# =============================================================== #
# ===================== tools/detect_fraud.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Detect potential fraud using hybrid (rules + ML)
# 🎯 Returns  : structured fraud case + risk score
# ✅ Used by  : flows.detect_and_escalate_flow, server, planner_agent
# =============================================================== #

from resources.vector_store.fraud_patterns import match_known_fraud_patterns
from tools.risk_scorer import calculate_risk_score
from tools.apply_rules import rule_check
from ml_models.behavior_baseline_model import score_behavior_anomaly
from ml_models.feature_engineering import extract_features

# =============================================================== #
# ============== HYBRID FRAUD DETECTION LOGIC =================== #
# =============================================================== #
def detect_fraud(transaction: dict) -> dict:
    """
    Detects potential fraud using a mix of heuristics and ML models.

    Args:
        transaction (dict): Incoming transaction data

    Returns:
        dict: Fraud case details including:
              - transaction_id
              - reason
              - rule_triggered
              - ml_score
              - risk_score
              - escalate (bool)
              - structured_case (dict)
    """

    if not transaction or not isinstance(transaction, dict):
        return {"error": "Invalid transaction input"}

    # ---------------------- #
    # 🧠 Extract Features
    # ---------------------- #
    features = extract_features(transaction)

    # ---------------------- #
    # 📏 Apply Rule Engine
    # ---------------------- #
    rule_result = rule_check(transaction)

    # ---------------------- #
    # 🤖 ML Model Score
    # ---------------------- #
    ml_score = score_behavior_anomaly(features)

    # ---------------------- #
    # 🧠 Risk Scoring
    # ---------------------- #
    risk_score = calculate_risk_score(rule_result, ml_score)

    # ---------------------- #
    # 🧩 Vector Match (optional)
    # ---------------------- #
    matched_pattern = match_known_fraud_patterns(transaction)

    escalate = risk_score > 75 or rule_result.get("flagged", False) or bool(matched_pattern)

    return {
        "transaction_id": transaction.get("transaction_id"),
        "reason": matched_pattern or rule_result.get("reason", "Suspicious activity detected"),
        "rule_triggered": rule_result,
        "ml_score": ml_score,
        "risk_score": risk_score,
        "escalate": escalate,
        "structured_case": {
            "account_id": transaction.get("account_id"),
            "amount": transaction.get("amount"),
            "location": transaction.get("location"),
            "method": transaction.get("method"),
            "flags": rule_result.get("flags", []),
            "ml_score": ml_score,
            "risk_score": risk_score,
        }
    }

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #