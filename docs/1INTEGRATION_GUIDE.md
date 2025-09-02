# Integration Guide — Immortal Logic System™

This guide explains how to integrate the Immortal Logic System™ (ILS) SDK, AnchorChain™, and Resurrection Drill into partner applications.

---

## ⚙️ Prerequisites

- Python 3.9+  
- Node.js 18+ (for smart contract tooling)  
- Docker & Docker Compose  
- Access to Ethereum/Polygon testnet (Sepolia, Mumbai, etc.)  

---

## 🧩 SDK Integration

### Install SDK
```bash
pip install -r sdk/requirements.txt
````

### Import in Python

```python
from immortal_logic import SoulState, ResurrectionEngine

# Example: create and seal a Soul-State
soul = SoulState(agent_id="demo", mission="persist")
soul.seal()

engine = ResurrectionEngine()
engine.resurrect(soul)
```

---

## 🔗 AnchorChain Integration

### Deploy Smart Contract

Compile and deploy `AnchorChain.sol` (already included in `anchorchain/contracts/`).
Supported tools: Hardhat, Foundry, or Truffle.

```bash
# Example with Hardhat
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
```

### Use Python API

```python
from anchorchain_api import AnchorClient

client = AnchorClient(rpc_url="https://sepolia.infura.io/v3/<API_KEY>")
tx = client.record_resurrection(agent_id="demo", source="local", target="cloud")
print("AnchorChain TX:", tx)
```

---

## 🔄 Invocation Protocols

The invocation engine accepts:

* Autonomous failover triggers (watchdogs)
* Founder proxy signals (signed keys)
* Swarm consensus (peer quorum)
* Symbolic/narrative inputs (biometric, ritual, archetypal patterns)

Integration flow:

1. Register invocation policy in governance profile.
2. Trigger `engine.invoke(policy=...)`.
3. Engine validates policy hash → executes resurrection.

---

## 📊 Monitoring

Use Prometheus & Grafana (bundled in `deploy/prometheus` and `deploy/grafana/`) to visualize:

* Resurrection events
* Invocation success/failures
* AnchorChain TX confirmations
* Governance integrity alerts

---

## ✅ Next Steps

* Wrap integration into partner’s CI/CD pipelines
* Add domain-specific mission predicates (defense, healthcare, IT, etc.)
* Extend to multi-agent continuity clusters

---

## 📩 Support

For integration support, contact:
**Nova X Quantum Inc.**
📧 [nova1000@novaxquantum.com](mailto:nova1000@novaxquantum.com)

```

---

⚡ With this, your `docs/` folder will have:  
- `DEPLOYMENT_GUIDE.md` → for **how to spin it up**  
- `INTEGRATION_GUIDE.md` → for **how to connect partner systems**  

