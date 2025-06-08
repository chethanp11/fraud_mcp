# =============================================================== #
# ==================== config/env_config.py ===================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Load environment variables and dynamic paths
# 📦 Loads    : .env file, config paths, model and DB locations
# ✅ Used by  : All MCP Servers and UI Clients
# =============================================================== #

import os
from dotenv import load_dotenv

# =============================================================== #
# =================== LOAD ENV VARIABLES ======================== #
# =============================================================== #
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

# --------------------------------------------------------------- #
# Runtime environment
# --------------------------------------------------------------- #
ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
PROJECT_NAME = os.getenv("PROJECT_NAME", "BankAI")

# --------------------------------------------------------------- #
# Path configurations
# --------------------------------------------------------------- #
CONFIG_PATH = os.path.join(ROOT_DIR, "config")
LOG_PATH = os.path.join(ROOT_DIR, "logging")
MEMORY_PATH = os.path.join(ROOT_DIR, "memory")
VECTOR_STORE_PATH = os.path.join(ROOT_DIR, "shared_libs", "vector_store")

# --------------------------------------------------------------- #
# External Keys and URLs (if any)
# --------------------------------------------------------------- #
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# =============================================================== #
# ======================= END OF FILE =========================== #
# =============================================================== #