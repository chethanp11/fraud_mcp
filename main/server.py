# =============================================================== #
# ====================== main/server.py ========================= #
# --------------------------------------------------------------- #
# 📌 Purpose   : Launch entrypoint for Fraud MCP Server
# 🛠  Mode     : CLI with basic routing and health check
# ✅ Called by : run_fraud_mcp.sh
# =============================================================== #

import uvicorn
import importlib
import pkgutil
import os
from fastapi import FastAPI
from config.env_config import load_env

# --------------------------------------------------------------- #
# Load environment config
# --------------------------------------------------------------- #
load_env()

# --------------------------------------------------------------- #
# Initialize FastAPI app
# --------------------------------------------------------------- #
app = FastAPI(title="Fraud MCP Server", version="1.0")

# =============================================================== #
# =============== REGISTERED TOOLS AND FLOWS ==================== #
# =============================================================== #
registered_tools = []
registered_flows = []

# --------------------------------------------------------------- #
# Tool discovery (from tools/*.py)
# --------------------------------------------------------------- #
def discover_tools():
    tools_pkg = "tools"
    for _, name, _ in pkgutil.iter_modules([tools_pkg]):
        if not name.startswith("_"):
            registered_tools.append(name)

# --------------------------------------------------------------- #
# Flow discovery (from flows/flow_registry.py)
# --------------------------------------------------------------- #
def discover_flows():
    try:
        flow_registry = importlib.import_module("flows.flow_registry")
        if hasattr(flow_registry, "list_registered_flows"):
            global registered_flows
            registered_flows = flow_registry.list_registered_flows()
    except Exception as e:
        print(f"⚠️ Failed to load flow registry: {e}")

# --------------------------------------------------------------- #
# Root route: show server summary
# --------------------------------------------------------------- #
@app.get("/")
def index():
    return {
        "message": "👋 Welcome to the Fraud MCP Server",
        "tools_registered": registered_tools,
        "flows_registered": registered_flows
    }

# --------------------------------------------------------------- #
# Health check route
# --------------------------------------------------------------- #
@app.get("/health")
def health_check():
    return {"status": "Fraud MCP is alive ✅"}

# =============================================================== #
# Server Execution
# =============================================================== #
if __name__ == "__main__":
    print("🔌 Starting Fraud MCP Server...")
    discover_tools()
    discover_flows()
    print(f"🧰 Tools: {registered_tools}")
    print(f"🔁 Flows: {registered_flows}")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)