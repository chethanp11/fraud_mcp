# =============================================================== #
# ====================== tools/apply_rules.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Evaluate transaction against YAML-defined fraud rules
# 🎯 Returns  : Dict indicating rule violations
# ✅ Used by  : tools.detect_fraud
# =============================================================== #

import yaml
import os

RULES_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "resources", "fraud_rules", "rules.yaml"
)

# =============================================================== #
# ===================== RULE CHECK FUNCTION ===================== #
# =============================================================== #
def rule_check(transaction: dict) -> dict:
    """
    Applies YAML-defined fraud rules to a given transaction.

    Args:
        transaction (dict): Input transaction details

    Returns:
        dict: {
            "flagged": bool,
            "reason": str,
            "flags": list of violated rule names
        }
    """
    try:
        with open(RULES_FILE_PATH, 'r') as file:
            rules = yaml.safe_load(file)
    except Exception as e:
        return {
            "flagged": False,
            "reason": f"Error loading rules: {str(e)}",
            "flags": []
        }

    flags = []
    for rule in rules.get("rules", []):
        rule_name = rule.get("name")
        condition = rule.get("condition")
        if not rule_name or not condition:
            continue

        try:
            # Evaluate condition using transaction context
            if eval(condition, {}, {"tx": transaction}):
                flags.append(rule_name)
        except Exception as e:
            continue  # skip faulty rule

    return {
        "flagged": bool(flags),
        "reason": f"Triggered rules: {', '.join(flags)}" if flags else "No rules triggered",
        "flags": flags
    }

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #