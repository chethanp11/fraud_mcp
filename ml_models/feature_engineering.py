# =============================================================== #
# =========== ml_models/feature_engineering.py ================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Extract and preprocess features from transaction data
# 🔍 Supports: fraud scoring, behavior modeling, rule matching
# 🎯 Returns  : Normalized feature dicts for modeling
# ✅ Used by  : detect_fraud.py, risk_scorer.py, behavior_baseline_model.py
# =============================================================== #

from datetime import datetime
from typing import Dict, Any

# =============================================================== #
# ====================== FEATURE EXTRACTOR ====================== #
# =============================================================== #

def extract_features(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts features from a raw transaction dictionary.

    Args:
        transaction (Dict): Input transaction with keys like:
            - amount, timestamp, location, merchant, type, device_id

    Returns:
        Dict[str, Any]: Processed feature dictionary
    """
    features = {}

    # Amount (log-scaled)
    amt = float(transaction.get("amount", 0.0))
    features["log_amount"] = round(0 if amt <= 0 else math.log1p(amt), 4)

    # Timestamp features
    ts = transaction.get("timestamp", "")
    try:
        dt = datetime.fromisoformat(ts)
        features["hour"] = dt.hour
        features["day_of_week"] = dt.weekday()
        features["is_weekend"] = int(dt.weekday() >= 5)
    except:
        features["hour"] = 12
        features["day_of_week"] = 0
        features["is_weekend"] = 0

    # Location and merchant
    features["location"] = transaction.get("location", "UNKNOWN").lower()
    features["merchant"] = transaction.get("merchant", "UNKNOWN").lower()

    # Transaction type
    features["txn_type"] = transaction.get("type", "UNKNOWN").lower()

    # Device ID presence
    features["has_device_id"] = int(bool(transaction.get("device_id")))

    return features

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #