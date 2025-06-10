# =============================================================== #
# =========== resources/monitoring/health_check.py ============== #
# --------------------------------------------------------------- #
# 📌 Purpose   : System health check for fraud MCP readiness
# 🔍 Checks    : DB connection, vector store, rules, memory files
# ✅ Used by   : Fraud Ops UI, CLI tools, DevOps monitors
# =============================================================== #

import os
import sqlite3

# =============================================================== #
# ========== CHECK DATABASE CONNECTIVITY ======================== #
# =============================================================== #
def check_database():
    """
    Verifies SQLite fraud case database is reachable and writable.
    """
    try:
        from ..db.fraud_cases_db import DB_PATH
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        return True, "Database connection: ✅"
    except Exception as e:
        return False, f"Database error: ❌ {e}"

# =============================================================== #
# ========== CHECK VECTOR STORE STATUS ========================== #
# =============================================================== #
def check_vector_store():
    """
    Dummy ping to check vector store interface (Qdrant or local stub).
    """
    try:
        from ..vector_store.fraud_patterns import ping_vector_store
        result = ping_vector_store()
        return True, f"Vector store: ✅ ({result})"
    except Exception as e:
        return False, f"Vector store error: ❌ {e}"

# =============================================================== #
# ========== CHECK FRAUD RULES YAML FILE ======================== #
# =============================================================== #
def check_rules_file():
    """
    Checks if fraud rules YAML file exists and is parsable.
    """
    try:
        from ..fraud_rules.rule_loader import load_rules
        rules = load_rules()
        return True, f"Fraud rules loaded: ✅ ({len(rules)} rules)"
    except Exception as e:
        return False, f"Rules error: ❌ {e}"

# =============================================================== #
# ========== CHECK MEMORY FILES PRESENCE ======================== #
# =============================================================== #
def check_memory_files():
    """
    Verifies that long-term and short-term memory JSONs are present.
    """
    try:
        from ...memory.long_term import LONG_TERM_FILE
        from ...memory.short_term import SHORT_TERM_FILE

        long_term_exists = os.path.exists(LONG_TERM_FILE)
        short_term_exists = os.path.exists(SHORT_TERM_FILE)

        if not long_term_exists or not short_term_exists:
            return False, "Memory file(s) missing ❌"

        return True, "Memory files present: ✅"
    except Exception as e:
        return False, f"Memory check error: ❌ {e}"

# =============================================================== #
# ========== AGGREGATE ALL HEALTH CHECKS ======================== #
# =============================================================== #
def run_all_checks():
    """
    Runs all individual checks and returns status dictionary.
    """
    results = {}
    for name, check in {
        "database": check_database,
        "vector_store": check_vector_store,
        "rules": check_rules_file,
        "memory": check_memory_files,
    }.items():
        status, msg = check()
        results[name] = msg
    return results

# =============================================================== #
# ========== OPTIONAL CLI ENTRY POINT =========================== #
# =============================================================== #
if __name__ == "__main__":
    print("🔎 Fraud MCP Health Check Summary:\n")
    result_map = run_all_checks()
    for k, v in result_map.items():
        print(f" - {v}")