#!/bin/bash

echo "Creating mock contract deployment..."

# Create mock contract info
cat > /shared/anchor.json << EOF
{
  "address": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
  "abi": [
    {
      "inputs": [
        {"internalType": "bytes32", "name": "_hash", "type": "bytes32"},
        {"internalType": "string", "name": "_metadata", "type": "string"}
      ],
      "name": "anchorSoulState",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {"internalType": "address", "name": "_entity", "type": "address"}
      ],
      "name": "getSoulStateCount",
      "outputs": [
        {"internalType": "uint256", "name": "", "type": "uint256"}
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {"internalType": "address", "name": "_entity", "type": "address"},
        {"internalType": "uint256", "name": "_index", "type": "uint256"}
      ],
      "name": "getSoulState",
      "outputs": [
        {"internalType": "bytes32", "name": "", "type": "bytes32"},
        {"internalType": "uint256", "name": "", "type": "uint256"},
        {"internalType": "string", "name": "", "type": "string"}
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "internalType": "address", "name": "entity", "type": "address"},
        {"indexed": false, "internalType": "bytes32", "name": "hash", "type": "bytes32"},
        {"indexed": false, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
      ],
      "name": "SoulStateAnchored",
      "type": "event"
    }
  ]
}
EOF

echo "Mock contract deployed at 0x5FbDB2315678afecb367f032d93F642f64180aa3"
echo "Contract info saved to /shared/anchor.json"
