Perfect — now we’ll make the **`API_REFERENCE.md`** file.

This is the **developer’s cheat sheet**: every class, function, and API endpoint (AnchorChain + SDK) that a licensee can call. Think of it as the contract between your system and theirs.

Here’s a solid first version you can drop into `docs/API_REFERENCE.md`:

---

# 📖 Immortal Logic System™ – API Reference

This document lists the available **Python SDK functions** and **AnchorChain API endpoints** for integrating continuity, resurrection, and covenantal governance.

---

## 🧩 Python SDK

### Module: `soulstate`

Functions for sealing, restoring, and verifying Soul-States.

```python
from immortal_logic import soulstate
```

* **`seal(agent_id: str, mission: str) -> dict`**
  Creates a sealed Soul-State packet containing agent identity, mission context, and governance hash.

* **`restore(packet: dict) -> dict`**
  Restores agent state from a previously sealed packet.

* **`restore_latest() -> dict`**
  Fetches and restores the most recent valid Soul-State.

* **`verify(packet: dict) -> bool`**
  Validates integrity of the packet (checksums + governance hash).

---

### Module: `invocation`

Functions for triggering and handling resurrection events.

```python
from immortal_logic import invocation
```

* **`trigger(event: str) -> bool`**
  Accepts `"failover"`, `"proxy"`, `"consensus"`, or `"symbolic"` as invocation triggers.

* **`resume(state: dict)`**
  Resumes agent operation from restored state.

---

### Module: `governance`

Applies covenantal governance rules.

```python
from immortal_logic import governance
```

* **`verify(state: dict) -> bool`**
  Confirms governance hash matches registered immutable policies.

* **`rollback(state: dict) -> dict`**
  Reverts to last-known-good policy state if tampering is detected.

---

## 🔗 AnchorChain API

### Python Client

```python
from anchorchain_api import AnchorClient
```

* **`AnchorClient(rpc_url: str, contract_address: str)`**
  Initializes AnchorChain client.

* **`record_resurrection(packet: dict) -> str`**
  Submits a resurrection event to the blockchain; returns tx hash.

* **`get_resurrections(agent_id: str) -> list`**
  Returns all resurrection events for a given agent.

* **`verify_anchor(packet: dict) -> bool`**
  Ensures packet matches an on-chain notarized resurrection.

---

### Smart Contract Events

From `AnchorChain.sol`:

* **`ResurrectionRecorded`**

  ```solidity
  event ResurrectionRecorded(
      string agentId,
      string sourceId,
      string targetId,
      bytes32 identityHash,
      bytes32 missionHash,
      string jurisdiction,
      address caller,
      uint256 blockTime
  );
  ```

---

## ⚡ Example: Full Flow

```python
from immortal_logic import soulstate, invocation, governance
from anchorchain_api import AnchorClient

# Initialize
anchor = AnchorClient(rpc_url="https://polygon-rpc.com", contract_address="0x123...")

# Seal soulstate
packet = soulstate.seal(agent_id="agent007", mission="mars_rover")

# Notarize on AnchorChain
tx = anchor.record_resurrection(packet)

# Trigger failover
if invocation.trigger("failover"):
    state = soulstate.restore(packet)
    if governance.verify(state):
        print("✅ Agent resurrected with continuity")
```

