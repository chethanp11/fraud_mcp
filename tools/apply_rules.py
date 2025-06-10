# =============================================================== #
# ====================== tools/apply_rules.py =================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Evaluate transaction against YAML-defined fraud rules
# 🎯 Returns  : Dict indicating rule violations with metadata
# ✅ Used by  : tools.detect_fraud
# =============================================================== #

import yaml
import os
import traceback
from tools.rule_trigger import enrich_triggered_rules  # 🚨 New module

RULES_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "resources", "fraud_rules", "rules.yaml"
)

# =============================================================== #
# ===================== RULE CHECK FUNCTION ===================== #
# =============================================================== #

def rule_check(transaction: dict) -> dict:
    """
    Applies YAML-defined fraud rules to a given transaction using dynamic conditions.

    Args:
        transaction (dict): Input transaction details (e.g., amount, location)

    Returns:
        dict: {
            "flagged": bool,
            "reason": str,
            "flags": list of violated rule names,
            "enriched": list of rule metadata (from rule_trigger)
        }
    """
    try:
        with open(RULES_FILE_PATH, 'r') as file:
            rules = yaml.safe_load(file)
    except Exception as e:
        return {
            "flagged": False,
            "reason": f"Error loading rules.yaml: {str(e)}",
            "flags": [],
            "enriched": []
        }

    triggered_flags = []
    for rule in rules.get("rules", []):
        rule_name = rule.get("name", "Unnamed Rule")
        condition = rule.get("condition")

        if not condition:
            continue

        try:
            # 🔐 Controlled eval scope: Only 'tx' is available
            if eval(condition, {}, {"tx": transaction}):
                triggered_flags.append(rule_name)
        except Exception:
            print(f"[Rule Eval Error] Skipping rule: {rule_name}\n{traceback.format_exc()}")

    # 🎯 Post-process using rule_trigger for enrichment
    enriched_metadata = enrich_triggered_rules(triggered_flags)

    return {
        "flagged": bool(triggered_flags),
        "reason": f"Triggered rules: {', '.join(triggered_flags)}" if triggered_flags else "No rules triggered",
        "flags": triggered_flags,
        "enriched": enriched_metadata
    }

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #