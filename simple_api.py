#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, Depends, Header
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from typing import Optional
import uvicorn
import hashlib
import time

app = FastAPI(title="AnchorChain API - Demo Mode")

# Prometheus metrics
tx_ok_counter = Counter('anchorchain_tx_ok', 'Successful anchor transactions')
tx_err_counter = Counter('anchorchain_tx_err', 'Failed anchor transactions')

def verify_token(authorization: Optional[str] = Header(None)):
    expected_token = "demo-token-123"
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if token == expected_token:
            return True
    # For demo, allow without token too
    return True

@app.get("/")
async def root():
    return {
        "message": "AnchorChain API - Demo Mode", 
        "status": "running",
        "contract": "0x1234567890abcdef1234567890abcdef12345678"
    }

@app.get("/metrics")
async def metrics():
    from fastapi import Response
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/anchor")
async def anchor_event(data: dict, _: bool = Depends(verify_token)):
    try:
        soul_id = data.get("soul_id", "unknown")
        state_hash = data.get("state_hash", "0x0")
        
        # Simulate blockchain transaction
        tx_hash = hashlib.sha256(f"{soul_id}{state_hash}{time.time()}".encode()).hexdigest()
        block_number = int(time.time()) % 1000000
        
        tx_ok_counter.inc()
        
        return {
            "success": True,
            "tx_hash": f"0x{tx_hash}",
            "block_number": block_number,
            "soul_id": soul_id,
            "state_hash": state_hash
        }
        
    except Exception as e:
        tx_err_counter.inc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting AnchorChain API - Demo Mode")
    print("📍 API: http://localhost:8000")
    print("📊 Metrics: http://localhost:8000/metrics")
    uvicorn.run(app, host="0.0.0.0", port=8000)
