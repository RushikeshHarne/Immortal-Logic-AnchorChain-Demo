# Immortal Logic Deployment Guide

## Docker Demo Stack

### Prerequisites
- Docker & Docker Compose installed
- 8GB+ RAM recommended
- Ports 3000, 8000, 8545, 9090 available

### Quick Start

#### Local Blockchain Demo
```bash
# Clone and setup
git clone https://github.com/Nova1000x/immortal-logic.git
cd immortal-logic

# Start local demo stack
docker compose --profile local up --build

# Wait for all services to start (2-3 minutes)
# Check logs: docker compose logs -f
```

#### Testnet Demo (Sepolia/Polygon Amoy)
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your testnet credentials:
# RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
# PRIVATE_KEY=0x1234567890abcdef... (funded testnet account)
# CHAIN_ID=11155111 (Sepolia) or 80002 (Polygon Amoy)

# Start testnet demo
docker compose --profile testnet --env-file .env up --build
```

### Service URLs
- **AnchorChain API**: http://localhost:8000
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus Metrics**: http://localhost:9090
- **Local Blockchain RPC**: http://localhost:8545

### Testing the Demo

#### Manual API Testing
```bash
# Health check
curl http://localhost:8000/health

# Check metrics
curl http://localhost:8000/metrics

# Anchor a soul state (requires Bearer token)
curl -X POST http://localhost:8000/anchor \
  -H "Authorization: Bearer demo-token-123" \
  -H "Content-Type: application/json" \
  -d '{"soul_hash": "test123", "metadata": "Demo resurrection event"}'
```

#### Automated Demo Script
```bash
# Install Python dependencies
pip install requests

# Run demo script
python sdk/drills/epls_demo.py --mode=local

# For testnet mode
python sdk/drills/epls_demo.py --mode=onchain --api-url=http://localhost:8000
```

### Monitoring

#### Grafana Dashboard
1. Open http://localhost:3000
2. Login: admin/admin
3. Navigate to "AnchorChain Metrics" dashboard
4. Monitor `anchorchain_tx_ok` and `anchorchain_tx_err` counters

#### Prometheus Metrics
- `anchorchain_tx_ok_total` - Successful transactions
- `anchorchain_tx_err_total` - Failed transactions

### Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Anvil/Hardhat │    │   Deployer       │    │  AnchorChain    │
│   (Blockchain)  │◄───┤   Container      │───►│  API            │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌────────▼────────┐              │
                       │  Shared Volume  │              │
                       │  /shared/anchor │              │
                       │  contract.json  │              │
                       └─────────────────┘              │
                                                        │
┌─────────────────┐    ┌──────────────────┐            │
│   Grafana       │◄───┤   Prometheus     │◄───────────┘
│   Dashboard     │    │   Metrics        │
└─────────────────┘    └──────────────────┘
```

### Troubleshooting

#### Common Issues

**Services not starting:**
```bash
# Check logs
docker compose logs -f

# Restart specific service
docker compose restart anchorchain-api
```

**Contract deployment failed:**
```bash
# Check deployer logs
docker compose logs deployer

# Verify blockchain is running
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

**API not connecting to contract:**
```bash
# Check shared volume
docker compose exec anchorchain-api ls -la /shared/anchor/

# Restart API after contract deployment
docker compose restart anchorchain-api
```

#### Clean Reset
```bash
# Stop all services
docker compose down

# Remove volumes and rebuild
docker compose down -v
docker compose --profile local up --build
```

### Security Notes (Demo Level)

- Default API token: `demo-token-123`
- Default private key is Anvil's first account (public knowledge)
- Services bind to localhost by default
- No TLS/HTTPS in demo mode
- Use throwaway testnet accounts only

### Production Considerations

For production deployment:
- Use proper secret management (AWS Secrets Manager, etc.)
- Enable TLS/HTTPS
- Implement proper authentication/authorization
- Use managed blockchain services
- Add proper logging and monitoring
- Implement backup and disaster recovery
- Use Kubernetes for orchestration
- Add rate limiting and DDoS protection
