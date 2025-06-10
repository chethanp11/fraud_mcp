# =============================================================== #
# ============ ml_models/behavior_baseline_model.py ============ #
# --------------------------------------------------------------- #
# 📌 Purpose   : Model user behavioral baselines for fraud detection
# 🔍 Learns normal transaction behavior (amounts, time, location)
# 🎯 Compares incoming data with baseline to flag anomalies
# ✅ Used by  : detect_fraud.py, risk_scorer.py
# =============================================================== #

import numpy as np
from datetime import datetime, time
from typing import List, Dict, Any

# =============================================================== #
# ============ BEHAVIOR BASELINE BUILDER & DETECTOR ============ #
# =============================================================== #

def build_baseline(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build behavioral baseline using past transaction data.

    Args:
        transactions (List[Dict]): List of transaction dicts with keys:
            - amount (float)
            - timestamp (str, ISO format)
            - location (str)

    Returns:
        Dict: Baseline profile with mean, std, time window, location freq
    """
    amounts = []
    hours = []
    location_counts = {}

    for txn in transactions:
        amt = txn.get("amount", 0.0)
        ts = txn.get("timestamp")
        loc = txn.get("location", "UNKNOWN")

        try:
            dt = datetime.fromisoformat(ts)
            hours.append(dt.hour)
        except:
            hours.append(12)  # Default to noon

        amounts.append(amt)
        location_counts[loc] = location_counts.get(loc, 0) + 1

    return {
        "amount_mean": np.mean(amounts) if amounts else 0,
        "amount_std": np.std(amounts) if amounts else 1,
        "hour_range": (min(hours), max(hours)) if hours else (8, 20),
        "common_locations": sorted(location_counts.items(), key=lambda x: -x[1])[:3]
    }

def is_anomalous(txn: Dict[str, Any], baseline: Dict[str, Any]) -> bool:
    """
    Compare transaction to baseline and flag if it deviates.

    Args:
        txn (Dict): Current transaction with keys like amount, timestamp, location
        baseline (Dict): Output of build_baseline()

    Returns:
        bool: True if anomalous, else False
    """
    amount = txn.get("amount", 0.0)
    ts = txn.get("timestamp")
    loc = txn.get("location", "")

    amount_z = abs((amount - baseline["amount_mean"]) / baseline["amount_std"])
    if amount_z > 3:
        return True

    try:
        txn_hour = datetime.fromisoformat(ts).hour
        min_hr, max_hr = baseline["hour_range"]
        if txn_hour < min_hr - 2 or txn_hour > max_hr + 2:
            return True
    except:
        return True

    locs = [x[0] for x in baseline["common_locations"]]
    if loc not in locs:
        return True

    return False

# =============================================================== #
# ======================== END OF FILE ========================= #
# =============================================================== #