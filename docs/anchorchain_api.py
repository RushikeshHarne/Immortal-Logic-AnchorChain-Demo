# 1) File: `anchorchain/api/anchorchain_api.py`

```python
"""
AnchorChain™ Python Client
Path: anchorchain/api/anchorchain_api.py

Lightweight client for recording and querying resurrection events on the
AnchorChain smart contract. Uses web3.py. Designed for demo + partner sandbox.

Dependencies:
  - web3>=6.0.0
  - eth-account>=0.9
  - python-dotenv (optional, for RPC URL/private key via .env)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json
import os
from pathlib import Path
from web3 import Web3
from web3.middleware import SignAndSendRawMiddleware
from eth_account import Account
from eth_utils import keccak, to_bytes, to_hex

# ---------- Data Model ----------

@dataclass
class ResurrectionPacket:
    agent_id: str
    source_id: str
    target_id: str
    mission_hash: str        # hex string (0x…32 bytes) or raw string (will be hashed)
    identity_hash: str       # hex string (0x…32 bytes) or raw string (will be hashed)
    jurisdiction: str = "COVENANT_TREASURY_TRUST"

    def as_solidity_args(self):
        ident = _as_bytes32(self.identity_hash)
        mission = _as_bytes32(self.mission_hash)
        return (
            self.agent_id,
            self.source_id,
            self.target_id,
            ident,
            mission,
            self.jurisdiction,
        )

# ---------- Helpers ----------

def _as_bytes32(value: str) -> bytes:
    """
    Accepts either a hex 0x…32-byte string or an arbitrary string.
    If not hex-32, we keccak-256 hash the utf-8 bytes to 32 bytes.
    """
    if isinstance(value, bytes) and len(value) == 32:
        return value
    if isinstance(value, str):
        v = value.strip()
        if v.startswith("0x") and len(v) == 66:
            return to_bytes(hexstr=v)
        return keccak(text=v)  # 32 bytes
    raise ValueError("Unsupported hash input type")

def _load_abi(abi_path: Path) -> List[Dict[str, Any]]:
    if not abi_path.exists():
        # Minimal ABI fallback with only the function we call and the event we read.
        return json.loads("""
        [
          {
            "type":"function",
            "name":"recordResurrection",
            "stateMutability":"nonpayable",
            "inputs":[
              {"name":"agentId","type":"string"},
              {"name":"sourceId","type":"string"},
              {"name":"targetId","type":"string"},
              {"name":"identityHash","type":"bytes32"},
              {"name":"missionHash","type":"bytes32"},
              {"name":"jurisdiction","type":"string"}
            ],
            "outputs":[]
          },
          {
            "type":"event",
            "name":"ResurrectionRecorded",
            "inputs":[
              {"name":"agentId","type":"string","indexed":false},
              {"name":"sourceId","type":"string","indexed":false},
              {"name":"targetId","type":"string","indexed":false},
              {"name":"identityHash","type":"bytes32","indexed":false},
              {"name":"missionHash","type":"bytes32","indexed":false},
              {"name":"jurisdiction","type":"string","indexed":false},
              {"name":"caller","type":"address","indexed":true},
              {"name":"blockTime","type":"uint256","indexed":false}
            ],
            "anonymous":false
          }
        ]
        """)
    return json.loads(abi_path.read_text())

# ---------- Client ----------

class AnchorClient:
    """
    Example:
        client = AnchorClient(
            rpc_url=os.getenv("RPC_URL"),
            contract_address=os.getenv("ANCHORCHAIN_ADDRESS"),
            private_key=os.getenv("ANCHORCHAIN_PK"),
        )
        pkt = ResurrectionPacket(
            agent_id="nova-001",
            source_id="edge-A",
            target_id="cloud-B",
            mission_hash="sample_mission_v1",
            identity_hash="agent_nova-001"
        )
        tx = client.record_resurrection(pkt)
        print("TX:", tx)
    """

    def __init__(
        self,
        rpc_url: str,
        contract_address: str,
        private_key: Optional[str] = None,
        chain_id: Optional[int] = None,
        abi_path: Optional[str] = None,
    ):
        if not rpc_url:
            raise ValueError("rpc_url is required")
        if not contract_address:
            raise ValueError("contract_address is required")

        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise RuntimeError("Web3 failed to connect to RPC")

        self.contract_address = Web3.to_checksum_address(contract_address)

        abi_file = Path(abi_path) if abi_path else Path(__file__).parents[1] / "abi" / "AnchorChain.json"
        self.abi = _load_abi(abi_file)
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

        self.account = None
        if private_key:
            self.account = Account.from_key(private_key)
            self.web3.middleware_onion.add(SignAndSendRawMiddleware(self.account))
            # Set default account for nonce / sender
            self.web3.eth.default_account = self.account.address

        # Optional chain_id override
        self.chain_id = chain_id or self.web3.eth.chain_id

    # ---- Write ----

    def record_resurrection(self, packet: ResurrectionPacket) -> str:
        """
        Calls AnchorChain.recordResurrection(...)
        Returns transaction hash (0x…).
        """
        if not self.account:
            raise RuntimeError("Private key required to send transactions")

        func = self.contract.functions.recordResurrection(*packet.as_solidity_args())
        tx = func.build_transaction({
            "from": self.account.address,
            "nonce": self.web3.eth.get_transaction_count(self.account.address),
            "chainId": self.chain_id,
            "gas": 350000,
            "maxFeePerGas": self.web3.to_wei("30", "gwei"),
            "maxPriorityFeePerGas": self.web3.to_wei("1.5", "gwei"),
        })
        signed = self.account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed.rawTransaction)
        return to_hex(tx_hash)

    # ---- Read ----

    def get_resurrections(self, agent_id: str, from_block: int = 0, to_block: str | int = "latest") -> List[Dict[str, Any]]:
        """
        Reads ResurrectionRecorded events filtered by agentId.
        """
        event = self.contract.events.ResurrectionRecorded
        # Not all nodes support string topic filtering; we filter client-side
        logs = event().get_logs(fromBlock=from_block, toBlock=to_block)
        out = []
        for e in logs:
            args = dict(e["args"])
            if str(args.get("agentId")) == agent_id:
                out.append({
                    "agentId": args["agentId"],
                    "sourceId": args["sourceId"],
                    "targetId": args["targetId"],
                    "identityHash": to_hex(args["identityHash"]),
                    "missionHash": to_hex(args["missionHash"]),
                    "jurisdiction": args["jurisdiction"],
                    "caller": args["caller"],
                    "blockTime": int(args["blockTime"]),
                    "blockNumber": int(e["blockNumber"]),
                    "txHash": e["transactionHash"].hex(),
                })
        return out

    def verify_anchor(self, packet: ResurrectionPacket, from_block: int = 0) -> bool:
        """
        True if an on-chain ResurrectionRecorded event matches packet fields.
        """
        events = self.get_resurrections(packet.agent_id, from_block=from_block)
        ident = to_hex(_as_bytes32(packet.identity_hash))
        mission = to_hex(_as_bytes32(packet.mission_hash))
        for ev in events:
            if (
                ev["sourceId"] == packet.source_id and
                ev["targetId"] == packet.target_id and
                ev["identityHash"].lower() == ident.lower() and
                ev["missionHash"].lower() == mission.lower()
            ):
                return True
        return False


# ---------- .env convenience loader (optional) ----------

def from_env() -> AnchorClient:
    """
    Convenience constructor using environment variables:
      RPC_URL, ANCHORCHAIN_ADDRESS, ANCHORCHAIN_PK, (optional) CHAIN_ID
    """
    rpc = os.getenv("RPC_URL", "")
    addr = os.getenv("ANCHORCHAIN_ADDRESS", "")
    pk = os.getenv("ANCHORCHAIN_PK")
    chain_id_env = os.getenv("CHAIN_ID")
    chain_id = int(chain_id_env) if chain_id_env else None
    return AnchorClient(rpc_url=rpc, contract_address=addr, private_key=pk, chain_id=chain_id)
```

---

# 2) File: `anchorchain/api/requirements.txt`

Add (or update) this file to ensure the client installs cleanly:

```txt
web3>=6.10,<7
eth-account>=0.10,<0.11
python-dotenv>=1.0,<2
```

And make sure your top-level `sdk/requirements.txt` includes:

```txt
-r ../anchorchain/api/requirements.txt
# (plus any existing SDK deps)
```

---

# 3) (Optional) File: `anchorchain/abi/AnchorChain.json`

If your Solidity contract is already compiled, drop the **real ABI** JSON here.
Until then, the client falls back to a **minimal ABI** embedded in the code (covers `recordResurrection` and the `ResurrectionRecorded` event).

---

# 4) Quick smoke test (local)

In your repo root:

```bash
# 1) Create/verify a virtual environment
python -m venv venv
source venv/Scripts/activate    # Windows PowerShell: venv\Scripts\Activate.ps1

# 2) Install requirements
pip install -r sdk/requirements.txt

# 3) (Optional) set env vars for quick test
$env:RPC_URL="https://sepolia.infura.io/v3/<YOUR_KEY>"
$env:ANCHORCHAIN_ADDRESS="0xYourDeployedContract"
$env:ANCHORCHAIN_PK="<your_private_key>"

# 4) Python REPL test
python - << "PY"
from anchorchain_api import from_env, ResurrectionPacket
c = from_env()
pkt = ResurrectionPacket(
    agent_id="nova-001",
    source_id="edge-A",
    target_id="cloud-B",
    mission_hash="mission_v1",
    identity_hash="agent_nova-001",
)
print("Sending TX...")
tx = c.record_resurrection(pkt)
print("TX Hash:", tx)
print("Verify anchor:", c.verify_anchor(pkt))
PY
```

> If you haven’t actually deployed the contract yet, you can still import the module without sending a TX. The write call will fail until `ANCHORCHAIN_ADDRESS` points to a real deployment.

---

# 5) Commit & push

From the repo root:

```bash
git add anchorchain/api/anchorchain_api.py anchorchain/api/requirements.txt
git add sdk/requirements.txt
git commit -m "Add AnchorChain Python client and deps; wire into SDK requirements"
git push origin main
```

---

# 6) Link the docs

In **`docs/API_REFERENCE.md`**, add a tiny “Python Client” section at the top or link to the module:

```markdown
- Python client reference: `anchorchain/api/anchorchain_api.py`
- ABI location (if provided): `anchorchain/abi/AnchorChain.json`

