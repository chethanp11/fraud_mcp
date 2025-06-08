# =============================================================== #
# =================== tools/risk_scorer.py ====================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Score incoming transactions or alerts for fraud risk
# 🔍 Uses rules + ML model features to compute composite score
# ✅ Used by   : detect_fraud.py, fraud_trends.py, analyst dashboard
# =============================================================== #

from tools.apply_rules import evaluate_rules
from ml_models.feature_engineering import extract_features
from ml_models.behavior_baseline_model import get_ml_risk_score

# =============================================================== #
# ======================== RISK SCORER ========================== #
# =============================================================== #
def compute_risk_score(transaction_data: dict) -> dict:
    """
    Computes a risk score for a transaction using rule-based
    scoring and ML model predictions.

    Args:
        transaction_data (dict): A single transaction dict

    Returns:
        dict: {
            "rule_score": float,
            "ml_score": float,
            "final_score": float,
            "verdict": "low" | "medium" | "high"
        }
    """
    # --- Rule-based score
    rule_score = evaluate_rules(transaction_data)

    # --- ML-based score
    features = extract_features(transaction_data)
    ml_score = get_ml_risk_score(features)

    # --- Composite final score (weighted average)
    final_score = round((0.6 * rule_score + 0.4 * ml_score), 2)

    # --- Verdict classification
    if final_score >= 0.8:
        verdict = "high"
    elif final_score >= 0.5:
        verdict = "medium"
    else:
        verdict = "low"

    return {
        "rule_score": round(rule_score, 2),
        "ml_score": round(ml_score, 2),
        "final_score": final_score,
        "verdict": verdict
    }

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #