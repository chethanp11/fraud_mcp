# =============================================================== #
# =============== resources/db/fraud_cases_db.py ================ #
# --------------------------------------------------------------- #
# 📌 Purpose   : Handles SQLite DB for fraud cases
# 🗂️ Tables     : fraud_cases
# 🔄 Supports   : insert, update, fetch by ID or status
# ✅ Used by   : tools, flows, UI components
# =============================================================== #

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "fraud_cases.db")

# =============================================================== #
# ========================= INIT SCHEMA ========================= #
# =============================================================== #

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS fraud_cases (
            case_id TEXT PRIMARY KEY,
            customer_id TEXT,
            status TEXT,
            risk_score INTEGER,
            created_at TEXT,
            updated_at TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()

# =============================================================== #
# ======================== DB OPERATIONS ======================== #
# =============================================================== #

def insert_case(case_id, customer_id, risk_score, metadata=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute("""
        INSERT INTO fraud_cases (case_id, customer_id, status, risk_score, created_at, updated_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (case_id, customer_id, "open", risk_score, timestamp, timestamp, metadata))
    conn.commit()
    conn.close()


def update_case_status(case_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute("""
        UPDATE fraud_cases
        SET status = ?, updated_at = ?
        WHERE case_id = ?
    """, (new_status, timestamp, case_id))
    conn.commit()
    conn.close()


def fetch_case(case_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM fraud_cases WHERE case_id = ?", (case_id,))
    row = c.fetchone()
    conn.close()
    return row


def fetch_cases_by_status(status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM fraud_cases WHERE status = ?", (status,))
    rows = c.fetchall()
    conn.close()
    return rows

# =============================================================== #
# ========================= END OF FILE ========================= #
# =============================================================== #