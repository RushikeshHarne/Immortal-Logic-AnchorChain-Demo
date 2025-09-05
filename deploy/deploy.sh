#!/bin/bash

echo "Waiting for blockchain to be ready..."

# Wait for RPC to be available
RPC_URL=${RPC_URL:-http://anvil:8545}
while ! curl -s -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' $RPC_URL > /dev/null; do
    echo "Waiting for blockchain at $RPC_URL..."
    sleep 5
done

echo "Blockchain ready, deploying contract..."

# Deploy contract
npx hardhat run scripts/deploy.js --network local

echo "Deployment complete!"
