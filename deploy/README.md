# AnchorChain Demo Stack

## 🎯 Project Overview

The AnchorChain Demo Stack is a complete containerized solution for demonstrating AI agent resurrection with blockchain notarization. This implementation consolidates all necessary components within the `deploy/` directory for clean project organization.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     Anvil       │    │   AnchorChain    │    │   Prometheus    │
│  Blockchain     │◄───┤      API         │◄───┤   Monitoring    │
│    :8545        │    │     :8080        │    │     :9090       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Contract      │    │    Grafana      │
                       │   Deployer      │    │  Dashboards     │
                       │   (one-time)    │    │     :3000       │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

Deploy the complete stack with a single command:

```bash
docker compose up --build
```

Test the deployment:

```bash
./demo_test.sh
```

## 📦 Components

### Services
- **Anvil**: Local Ethereum blockchain for testing
- **Deployer**: One-time contract deployment service
- **AnchorChain API**: FastAPI service with Prometheus metrics
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Dashboard visualization

### Key Files
- `docker-compose.yml` - Complete service orchestration
- `Dockerfile.api` - AnchorChain API container
- `api/main.py` - FastAPI application with Web3 integration
- `contracts/AnchorChain.sol` - Smart contract for soul state anchoring
- `prometheus/prometheus.yml` - Monitoring configuration
- `grafana/provisioning/` - Dashboard and datasource configs

## 🎮 API Endpoints

- `GET /health` - Service health and mode status
- `POST /anchor` - Anchor soul state with metadata
- `GET /soul-state/{address}` - Retrieve anchored states
- `GET /metrics` - Prometheus metrics endpoint
- `GET /docs` - Interactive API documentation

## 📊 Metrics

- `anchorchain_tx_ok_total` - Successful transactions
- `anchorchain_tx_err_total` - Failed transactions

## 🔧 Configuration

Environment variables (see `.env.example`):
- `RPC_URL` - Blockchain RPC endpoint
- `PRIVATE_KEY` - Deployment account private key
- `CHAIN_ID` - Network chain ID

## 🌐 Access Points

- **AnchorChain API**: http://localhost:8080
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## ✅ Success Criteria

All deliverables completed:
- ✅ Complete `deploy/` folder with all configs
- ✅ `.env.example` file with documentation
- ✅ Comprehensive deployment guide
- ✅ Working demo with metrics integration
- ✅ One-command deployment
- ✅ Mock mode fallback for reliability

## 🎯 Demo Flow

1. **Start Stack**: `docker compose up --build`
2. **Deploy Contract**: Automatic via deployer service
3. **Test API**: Health checks and soul state anchoring
4. **Monitor Metrics**: Prometheus collection and Grafana visualization
5. **Verify Integration**: End-to-end transaction flow

## 🛠️ Development

For development and testing:

```bash
# Start services
docker compose up --build -d

# Run tests
./demo_test.sh

# Check logs
docker compose logs -f anchorchain-api

# Cleanup
docker compose down -v
```

## 📈 Production Readiness

Current implementation provides:
- Containerized deployment
- Monitoring integration
- Health checks
- Error handling
- Mock mode fallback
- Comprehensive documentation

For production deployment, consider:
- Real testnet integration
- Security hardening
- Persistent storage
- Load balancing
- Advanced monitoring

## 🎉 Project Status

**COMPLETE** - All Phase 1 requirements fulfilled with working demo stack.
