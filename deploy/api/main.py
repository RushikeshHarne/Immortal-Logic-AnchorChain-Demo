import os
import json
from fastapi import FastAPI, HTTPException, Depends, Header
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from web3 import Web3
from typing import Optional
import uvicorn

app = FastAPI(title="AnchorChain API")

# Prometheus metrics
tx_ok_counter = Counter('anchorchain_tx_ok', 'Successful anchor transactions')
tx_err_counter = Counter('anchorchain_tx_err', 'Failed anchor transactions')

# Global variables
w3 = None
contract = None
contract_address = None

def load_contract():
    global w3, contract, contract_address
    
    try:
        # Load contract info from shared volume
        with open('/shared/anchor/contract.json', 'r') as f:
            contract_info = json.load(f)
        
        contract_address = contract_info['address']
        abi = contract_info['abi']
        
        # Connect to blockchain
        rpc_url = os.getenv('RPC_URL', 'http://anvil:8545')
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Load contract
        contract = w3.eth.contract(address=contract_address, abi=abi)
        
        return True
    except Exception as e:
        print(f"Failed to load contract: {e}")
        return False

def verify_token(authorization: Optional[str] = Header(None)):
    expected_token = os.getenv('API_TOKEN', 'demo-token-123')
    if not authorization or authorization != f"Bearer {expected_token}":
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def root():
    return {"message": "AnchorChain API running", "contract": contract_address}

@app.get("/metrics")
async def metrics():
    from fastapi import Response
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/anchor")
async def anchor_event(
    soul_id: str,
    state_hash: str,
    _: str = Depends(verify_token)
):
    if not contract:
        raise HTTPException(status_code=503, detail="Contract not loaded")
    
    try:
        # Get account (for demo, use first account)
        accounts = w3.eth.accounts
        if not accounts:
            # For testnet, we need to add the private key
            private_key = os.getenv('PRIVATE_KEY')
            if private_key:
                account = w3.eth.account.from_key(private_key)
                w3.eth.default_account = account.address
            else:
                raise Exception("No accounts available")
        else:
            w3.eth.default_account = accounts[0]
        
        # Call contract
        tx_hash = contract.functions.anchorSoulState(
            soul_id, state_hash
        ).transact()
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        tx_ok_counter.inc()
        
        return {
            "success": True,
            "tx_hash": tx_hash.hex(),
            "block_number": receipt.blockNumber
        }
        
    except Exception as e:
        tx_err_counter.inc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Wait for contract to be deployed
    import time
    while not load_contract():
        print("Waiting for contract deployment...")
        time.sleep(5)
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    
    print(f"Starting AnchorChain API at http://{host}:{port}")
    print(f"Grafana dashboard: http://localhost:3000")
    
    uvicorn.run(app, host=host, port=port)
