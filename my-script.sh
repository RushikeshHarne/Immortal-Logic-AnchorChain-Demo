#!/bin/bash

# ==============================================================================
# Immortal Logic - Full Demo Deployment and Testing Script
#
# This script automates the end-to-end process of setting up the Immortal Logic
# demo stack, as described in the provided DEPLOYMENT_GUIDE.md and other docs.
# It handles local and testnet deployments, API testing, and provides
# troubleshooting commands.
# ==============================================================================

# --- Function to check for a command's existence ---
command_exists () {
  command -v "$1" >/dev/null 2>&1
}

# --- Section 1: Prerequisites Check ---
echo "--- Checking Prerequisites ---"
echo "This script requires Docker, Docker Compose, and Python 3. You should also have at least 8GB of RAM available."
if ! command_exists docker; then
  echo "Error: Docker is not installed. Please install Docker and try again."
  exit 1
fi
if ! command_exists docker-compose; then
  echo "Warning: 'docker-compose' command not found. Using 'docker compose'."
fi
if ! command_exists python3; then
  echo "Error: Python 3 is not installed. Please install Python 3 and ensure it's in your PATH."
  exit 1
fi
echo "Prerequisites met. Proceeding with deployment..."
echo ""

# --- Section 2: Local Blockchain Demo Setup ---
echo "--- Starting Local Blockchain Demo Stack ---"
echo "This will build and start the Anvil blockchain, the Deployer, the AnchorChain API, and the monitoring services (Grafana & Prometheus)."
echo "The services will run in the background (detached mode)."
echo ""

# The user-provided DEPLOYMENT_GUIDE.md uses `docker compose`.
# This is the modern syntax. We'll stick to that.
docker compose --profile local up --build -d

if [ $? -eq 0 ]; then
  echo ""
  echo "Docker stack started successfully. Waiting 30 seconds for services to become ready..."
  sleep 30
  echo ""
  echo "You can check the logs to monitor service startup:"
  echo "docker compose logs -f"
  echo ""
else
  echo "Error: Failed to start the Docker stack. Please check the error messages above."
  exit 1
fi

# --- Section 3: API and Automated Testing ---
echo "--- Running API Health and Metrics Checks ---"
# Give the API a few seconds to start up and connect to the blockchain.
sleep 5
echo "Running API health check:"
curl http://localhost:8000/health
echo ""
echo "Running API metrics check:"
curl http://localhost:8000/metrics
echo ""

echo "--- Running Automated Demo Script ---"
echo "This will install Python dependencies and run the epls_demo.py script to test the system."
echo ""
pip install requests
python3 sdk/drills/epls_demo.py --mode=local

echo ""
echo "--- Automated Testing Complete ---"
echo "Check the output above for results."
echo ""

# --- Section 4: Monitoring and Troubleshooting ---
echo "--- Monitoring & Service URLs ---"
echo "You can now access the following services:"
echo " - AnchorChain API: http://localhost:8000"
echo " - Grafana Dashboard: http://localhost:3000 (Login: admin/admin)"
echo " - Prometheus Metrics: http://localhost:9090"
echo " - Local Blockchain RPC: http://localhost:8545"
echo ""

echo "--- Troubleshooting ---"
echo "If you encounter any issues, you can use these commands:"
echo " - Stop and remove all containers: docker compose down"
echo " - Stop, remove containers and volumes for a clean reset: docker compose down -v"
echo " - Restart a specific service: docker compose restart anchorchain-api"
echo " - View live logs: docker compose logs -f"
echo ""

# --- Section 5: Testnet Demo (Manual Interaction) ---
echo "--- Testnet Demo Configuration (Optional) ---"
echo "You can now stop the local demo and start a testnet demo."
read -p "Would you like to configure and start the Testnet Demo? (y/n): " confirm_testnet
if [[ "$confirm_testnet" == "y" || "$confirm_testnet" == "Y" ]]; then
  echo ""
  echo "First, stopping the local demo..."
  docker compose down
  echo ""
  echo "Now, please provide your testnet credentials to create the .env file."
  read -p "Enter your RPC_URL (e.g., https://sepolia.infura.io/v3/YOUR_PROJECT_ID): " rpc_url
  read -p "Enter your PRIVATE_KEY (0x...): " private_key
  read -p "Enter the CHAIN_ID (e.g., 11155111 for Sepolia): " chain_id

  # Create the .env file with user input
  echo "RPC_URL=$rpc_url" > .env
  echo "PRIVATE_KEY=$private_key" >> .env
  echo "CHAIN_ID=$chain_id" >> .env

  echo ""
  echo "Starting the Testnet Demo Stack..."
  docker compose --profile testnet --env-file .env up --build -d
  echo ""
  echo "Testnet stack started. You can now run the on-chain drill:"
  echo "python3 sdk/drills/epls_demo.py --mode=onchain --api-url=http://localhost:8000"
else
  echo ""
  echo "Testnet demo skipped. The script has finished."
fi
