# =============================================================== #
# =========== resources/fraud_rules/rule_loader.py ============== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Load and parse fraud detection rules from YAML
# 📄 Format    : rules.yaml with structured rule blocks
# ✅ Used by   : tools/apply_rules.py
# =============================================================== #

import os
import yaml

RULES_FILE = os.path.join(os.path.dirname(__file__), "rules.yaml")

# =============================================================== #
# ======================= RULE LOADER CORE ====================== #
# =============================================================== #

def load_fraud_rules() -> list[dict]:
    """
    Loads structured fraud rules from the YAML config file.

    Returns:
        list[dict]: List of parsed fraud rules
    """
    if not os.path.exists(RULES_FILE):
        raise FileNotFoundError(f"Rules file not found: {RULES_FILE}")

    with open(RULES_FILE, "r") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, list):
        raise ValueError("Rules file must contain a list of rule definitions.")

    return data

# =============================================================== #
# ====================== SAMPLE RULE FORMAT ===================== #
# - id: rule_001
#   name: High Value Foreign Transaction
#   description: Flag if transaction > $10,000 and not in home country
#   conditions:
#     - field: amount
#       operator: gt
#       value: 10000
#     - field: country
#       operator: ne
#       value: "IN"
#   severity: high
# =============================================================== #

# ======================== END OF FILE ========================== #