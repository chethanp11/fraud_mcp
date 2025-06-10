# =============================================================== #
# ========== resources/fraud_rules/rule_trigger.py ============== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Evaluate YAML-based fraud rules on transaction data
# 🔍 Rules     : Loaded via rule_loader, applied per transaction
# ✅ Used by   : apply_rules.py
# =============================================================== #

from .rule_loader import load_rules

# =============================================================== #
# =============== RULE TRIGGER EVALUATOR ======================== #
# =============================================================== #

def evaluate_rules(transaction: dict) -> list[dict]:
    """
    Evaluate all fraud rules against a transaction and return matched ones.

    Args:
        transaction (dict): The transaction input with necessary fields

    Returns:
        list[dict]: List of rules that were triggered
    """
    rules = load_rules()
    triggered = []

    for rule in rules:
        field = rule.get("field")
        condition = rule.get("condition")
        threshold = rule.get("threshold")

        value = transaction.get(field)

        # Ignore if field is missing in transaction
        if value is None:
            continue

        # ---------------------------- #
        # Basic Condition Matching
        # ---------------------------- #
        if condition == "greater_than" and value > threshold:
            triggered.append(rule)
        elif condition == "less_than" and value < threshold:
            triggered.append(rule)
        elif condition == "equals" and value == threshold:
            triggered.append(rule)
        elif condition == "not_equals" and value != threshold:
            triggered.append(rule)
        elif condition == "contains" and isinstance(value, str) and threshold in value:
            triggered.append(rule)
        # Extend with more rule types if needed

    return triggered

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #