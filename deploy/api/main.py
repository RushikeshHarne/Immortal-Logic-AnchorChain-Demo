import json
import os
from fastapi import FastAPI, HTTPException, Depends, Header
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from web3 import Web3
from typing import Optional
import time

app = FastAPI(title="AnchorChain API", description="Immortal Logic AnchorChain API")

# Prometheus metrics
tx_ok_counter = Counter('anchorchain_tx_ok', 'Successful AnchorChain transactions')
tx_err_counter = Counter('anchorchain_tx_err', 'Failed AnchorChain transactions')

# Configuration
API_TOKEN = os.getenv('API_TOKEN', 'demo-token-123')
RPC_URL = os.getenv('RPC_URL', 'http://anvil:8545')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

# Web3 setup
w3 = None
contract = None
account = None

def load_contract():
    global w3, contract, account
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        
        # Load contract from shared volume
        contract_path = '/shared/anchor/contract.json'
        if os.path.exists(contract_path):
            with open(contract_path, 'r') as f:
                contract_data = json.load(f)
            
            contract = w3.eth.contract(
                address=contract_data['address'],
                abi=contract_data['abi']
            )
            
            if PRIVATE_KEY:
                account = w3.eth.account.from_key(PRIVATE_KEY)
            
            return True
    except Exception as e:
        print(f"Contract loading error: {e}")
    return False

def verify_token(authorization: Optional[str] = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid token")

@app.on_event("startup")
async def startup():
    # Wait for contract deployment
    for _ in range(30):
        if load_contract():
            break
        time.sleep(2)

@app.get("/")
async def root():
    return {"message": "AnchorChain API running", "status": "ok"}

@app.get("/health")
async def health():
    contract_loaded = contract is not None
    return {
        "status": "healthy",
        "contract_loaded": contract_loaded,
        "rpc_url": RPC_URL,
        "chain_connected": w3.is_connected() if w3 else False
    }

from pydantic import BaseModel

class AnchorRequest(BaseModel):
    soul_hash: str
    metadata: str = ""

@app.post("/anchor")
async def anchor_soul_state(
    request: AnchorRequest,
    _: str = Depends(verify_token)
):
    try:
        if not contract or not account:
            raise HTTPException(status_code=503, detail="Contract not available")
        
        # Convert soul_hash to bytes32
        hash_bytes = Web3.keccak(text=request.soul_hash)
        
        # Build transaction
        tx = contract.functions.anchorSoulState(hash_bytes, request.metadata).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        
        # Sign and send
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        tx_ok_counter.inc()
        
        return {
            "transaction_hash": receipt.transactionHash.hex(),
            "block_number": receipt.blockNumber,
            "status": "success",
            "gas_used": receipt.gasUsed
        }
        
    except Exception as e:
        tx_err_counter.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/soul-state/{address}")
async def get_soul_states(address: str):
    try:
        if not contract:
            raise HTTPException(status_code=503, detail="Contract not available")
        
        count = contract.functions.getSoulStateCount(address).call()
        states = []
        
        for i in range(count):
            state = contract.functions.getSoulState(address, i).call()
            states.append({
                "hash": state[0].hex(),
                "timestamp": state[1],
                "metadata": state[2]
            })
        
        return {"address": address, "states": states, "count": count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
