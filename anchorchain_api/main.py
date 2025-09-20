from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from web3 import Web3
import json
import os
import time
from starlette.responses import Response

app = FastAPI()

# Prometheus metrics
anchorchain_tx_ok = Counter('anchorchain_tx_ok_total', 'Successful AnchorChain transactions')
anchorchain_tx_err = Counter('anchorchain_tx_err_total', 'Failed AnchorChain transactions')
resurrection_verify_pass = Counter('resurrection_verify_pass_total', 'Successful resurrection verifications')
resurrection_verify_fail = Counter('resurrection_verify_fail_total', 'Failed resurrection verifications')
gas_cost_histogram = Histogram('anchorchain_gas_cost', 'Gas cost of transactions')
anchorchain_tx_confirm_time_seconds = Histogram('anchorchain_tx_confirm_time_seconds', 'Transaction confirmation time')

# Web3 setup
rpc_url = os.getenv('RPC_URL', 'http://ganache:8545')
private_key = os.getenv('PRIVATE_KEY')
chain_id = int(os.getenv('CHAIN_ID', '1337'))
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Load contract
contract_address = None
contract_abi = None

try:
    with open('/shared/anchor/deployment.json', 'r') as f:
        deployment = json.load(f)
        contract_address = deployment['address']
        contract_abi = deployment['abi']
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
except:
    contract = None

@app.get("/")
async def root():
    return {"status": "AnchorChain API running", "contract": contract_address, "chain_id": chain_id, "rpc_url": rpc_url}

@app.get("/contract-info")
async def contract_info():
    if not contract:
        raise HTTPException(status_code=500, detail="Contract not loaded")
    
    # Get network info
    network_name = "Polygon Amoy" if chain_id == 80002 else "Sepolia" if chain_id == 11155111 else "Local"
    explorer_url = f"https://amoy.polygonscan.com/address/{contract_address}" if chain_id == 80002 else f"https://sepolia.etherscan.io/address/{contract_address}" if chain_id == 11155111 else None
    
    return {
        "contract_address": contract_address,
        "chain_id": chain_id,
        "network": network_name,
        "explorer_url": explorer_url,
        "rpc_url": rpc_url
    }

@app.post("/anchor/{soul_hash}")
async def anchor_resurrection(soul_hash: str):
    """Main anchor endpoint for resurrection notarization"""
    if not contract:
        anchorchain_tx_err.inc()
        raise HTTPException(status_code=500, detail="Contract not loaded")
    
    try:
        start_time = time.time()
        account = w3.eth.account.from_key(private_key)
        
        # Build transaction - Convert to bytes32
        hash_bytes = bytes.fromhex(soul_hash.replace('0x', ''))
        if len(hash_bytes) != 32:
            # Pad or truncate to 32 bytes
            hash_bytes = hash_bytes.ljust(32, b'\x00')[:32]
        tx = contract.functions.notarizeResurrection(hash_bytes).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'chainId': chain_id
        })
        
        # Sign and send
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Record metrics
        confirmation_time = time.time() - start_time
        gas_used = receipt['gasUsed']
        
        anchorchain_tx_ok.inc()
        gas_cost_histogram.observe(gas_used)
        anchorchain_tx_confirm_time_seconds.observe(confirmation_time)
        
        # Generate explorer URL
        explorer_tx_url = None
        if chain_id == 80002:
            explorer_tx_url = f"https://amoy.polygonscan.com/tx/{tx_hash.hex()}"
        elif chain_id == 11155111:
            explorer_tx_url = f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}"
        
        return {
            "tx_hash": tx_hash.hex(),
            "gas_used": gas_used,
            "confirmation_time": confirmation_time,
            "block_number": receipt['blockNumber'],
            "explorer_url": explorer_tx_url,
            "chain_id": chain_id,
            "event": "ResurrectionRecorded"
        }
    except Exception as e:
        anchorchain_tx_err.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notarize/{soul_hash}")
async def notarize_resurrection(soul_hash: str):
    # Redirect to anchor endpoint
    return await anchor_resurrection(soul_hash)

@app.post("/verify/{soul_hash}")
async def verify_resurrection(soul_hash: str):
    if not contract:
        resurrection_verify_fail.inc()
        raise HTTPException(status_code=500, detail="Contract not loaded")
    
    try:
        account = w3.eth.account.from_key(private_key)
        
        # Build transaction - Convert to bytes32
        hash_bytes = bytes.fromhex(soul_hash.replace('0x', ''))
        if len(hash_bytes) != 32:
            hash_bytes = hash_bytes.ljust(32, b'\x00')[:32]
        tx = contract.functions.verifyResurrection(hash_bytes).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'chainId': chain_id
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Generate explorer URL
        explorer_tx_url = None
        if chain_id == 80002:
            explorer_tx_url = f"https://amoy.polygonscan.com/tx/{tx_hash.hex()}"
        elif chain_id == 11155111:
            explorer_tx_url = f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}"
        
        resurrection_verify_pass.inc()
        return {
            "tx_hash": tx_hash.hex(), 
            "verified": True,
            "block_number": receipt['blockNumber'],
            "explorer_url": explorer_tx_url,
            "chain_id": chain_id
        }
    except Exception as e:
        resurrection_verify_fail.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "contract_loaded": contract is not None}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
