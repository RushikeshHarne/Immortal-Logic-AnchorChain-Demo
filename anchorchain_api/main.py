import json
import os
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI(title="AnchorChain API")

# Prometheus metrics
tx_ok_counter = Counter('anchorchain_tx_ok', 'Successful AnchorChain transactions')
tx_err_counter = Counter('anchorchain_tx_err', 'Failed AnchorChain transactions')

# Mock data for testing
mock_contract_deployed = True
mock_transactions = []

@app.get("/health")
async def health():
    return {"status": "healthy", "contract_loaded": mock_contract_deployed}

@app.post("/anchor")
async def anchor_soul_state(soul_hash: str, metadata: str = ""):
    try:
        # Mock successful transaction
        mock_tx = {
            "transaction_hash": f"0x{soul_hash}abc123",
            "block_number": len(mock_transactions) + 1,
            "soul_hash": soul_hash,
            "metadata": metadata,
            "timestamp": "2025-09-04T06:47:00Z"
        }
        mock_transactions.append(mock_tx)
        tx_ok_counter.inc()
        
        return {
            "transaction_hash": mock_tx["transaction_hash"],
            "block_number": mock_tx["block_number"],
            "status": "success"
        }
    except Exception as e:
        tx_err_counter.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/soul-state/{address}")
async def get_soul_states(address: str):
    # Return mock data for any address
    states = [tx for tx in mock_transactions]
    return {"address": address, "states": states}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
