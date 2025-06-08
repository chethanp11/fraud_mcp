#!/bin/bash
# =============================================================== #
# ==================== run_fraud_mcp.sh ========================= #
# --------------------------------------------------------------- #
# 📌 Purpose : Launch the Fraud MCP Server with proper config
# 🛠  Uses   : Activates venv, sets PYTHONPATH, runs server
# =============================================================== #

# Activate virtual environment
source ~/venvs/bankai_env/bin/activate

# Set working directory to fraud_mcp root
cd ~/Dev/BankAI/bank_verticals/fraud_mcp || exit

# Export PYTHONPATH for modular imports
export PYTHONPATH=~/Dev/BankAI/shared_libs:~/Dev/BankAI/config:.

# Launch the MCP server
echo "🚀 Launching Fraud MCP Server..."
python3 main/server.py