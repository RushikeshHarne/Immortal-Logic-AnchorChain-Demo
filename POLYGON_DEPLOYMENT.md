# Polygon Amoy Deployment Guide

## Prerequisites

1. **Polygon Amoy Testnet Setup:**
   - Get MATIC tokens from [Polygon Faucet](https://faucet.polygon.technology/)
   - Private key with sufficient MATIC balance
   - MetaMask configured for Polygon Amoy

2. **Required Tools:**
   ```bash
   pip install web3 py-solc-x fastapi uvicorn
   ```

## Step 1: Deploy Smart Contract

1. **Set environment variables:**
   ```bash
   export PRIVATE_KEY="your_private_key_here"
   ```

2. **Deploy contract:**
   ```bash
   cd anchorchain
   python deploy.py
   ```

3. **Verify deployment:**
   - Check `deployment.json` for contract address
   - Visit https://amoy.polygonscan.com/address/YOUR_CONTRACT_ADDRESS

## Step 2: Configure Kubernetes Secrets

1. **Update secret values:**
   ```bash
   # Edit deploy/k8s/anchorchain-secrets.yaml
   # Replace YOUR_PRIVATE_KEY_HERE and YOUR_CONTRACT_ADDRESS_HERE
   ```

2. **Apply secrets:**
   ```bash
   kubectl apply -f deploy/k8s/anchorchain-secrets.yaml
   ```

## Step 3: Build and Deploy API

1. **Build Docker image:**
   ```bash
   cd anchorchain
   docker build -t anchorchain-api:latest .
   ```

2. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f deploy/k8s/anchorchain-secrets.yaml
   ```

## Step 4: Test Integration

1. **Run end-to-end test:**
   ```bash
   python test_polygon_integration.py
   ```

2. **Manual API test:**
   ```bash
   curl -X POST "http://localhost:8000/anchor" \
     -H "Content-Type: application/json" \
     -d '{
       "agentId": "test-001",
       "sourceEmbodimentId": "alpha",
       "targetEmbodimentId": "beta", 
       "identityHash": "test-hash-123",
       "missionHash": "mission-456",
       "jurisdiction": "NOVA-1000"
     }'
   ```

## Step 5: Monitor Metrics

1. **Check Prometheus metrics:**
   ```bash
   curl http://localhost:8000/metrics
   ```

2. **Key metrics to monitor:**
   - `anchorchain_tx_success_total`
   - `anchorchain_tx_cost_gwei`
   - `anchorchain_tx_confirm_time_seconds`
   - `resurrection_verify_pass_total`

## Verification Checklist

- [ ] Contract deployed to Polygon Amoy
- [ ] Transaction visible on Amoy explorer
- [ ] API responds to /health endpoint
- [ ] Successful /anchor request
- [ ] Metrics updating in Prometheus
- [ ] Kubernetes secrets configured
- [ ] End-to-end test passes

## Troubleshooting

**Connection Issues:**
- Verify RPC URL: https://rpc-amoy.polygon.technology
- Check MATIC balance for gas fees

**Transaction Failures:**
- Increase gas limit in deploy.py
- Verify private key has sufficient funds

**Metrics Not Updating:**
- Check Prometheus scrape configuration
- Verify /metrics endpoint accessibility
