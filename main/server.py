# =============================================================== #
# ====================== main/server.py ========================= #
# --------------------------------------------------------------- #
# 📌 Purpose   : Launch entrypoint for Fraud MCP Server
# 🛠  Mode     : CLI with basic routing and health check
# ✅ Called by : run_fraud_mcp.sh
# =============================================================== #

import uvicorn
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
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)