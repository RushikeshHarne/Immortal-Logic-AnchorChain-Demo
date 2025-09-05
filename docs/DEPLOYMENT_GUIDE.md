# AnchorChain Deployment Guide

## Docker Demo Stack

### Local Development (Anvil Chain)

```bash
# Start local demo stack
cd deploy/
docker compose --profile local up --build

# Access points:
# - API: http://localhost:8000
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
# - Blockchain RPC: http://localhost:8545
```

### Testnet Mode (Sepolia/Polygon Amoy)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your testnet credentials:
# RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
# PRIVATE_KEY=0x...
# CHAIN_ID=11155111

# Start testnet stack
docker compose --profile testnet --env-file .env up --build
```

### Testing the API

```bash
# Run demo script
python sdk/drills/epls_demo.py --mode=local

# Manual API test
curl http://localhost:8000/
curl -H "Authorization: Bearer demo-token-123" \
     -H "Content-Type: application/json" \
     -d '{"soul_id":"test-001","state_hash":"0xabc123"}' \
     http://localhost:8000/anchor
```

### Monitoring

- **Grafana Dashboard**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`
  - View AnchorChain metrics: `anchorchain_tx_ok` and `anchorchain_tx_err`

- **Prometheus**: http://localhost:9090
  - Direct metrics access: http://localhost:8000/metrics

### Cleanup

```bash
# Stop all services
docker compose --profile local down
docker compose --profile testnet down

# Remove volumes
docker compose down -v
```

## Architecture

1. **Anvil/Testnet**: Local blockchain or external testnet
2. **Deployer**: Compiles and deploys AnchorChain.sol contract
3. **API**: FastAPI service exposing `/anchor` endpoint
4. **Prometheus**: Scrapes metrics from API
5. **Grafana**: Visualizes transaction success/failure rates

## Security Notes

- Demo uses bearer token authentication (`API_TOKEN`)
- Local mode binds to `0.0.0.0`, testnet mode to `127.0.0.1`
- Never commit private keys to version control
- Use throwaway testnet keys only
