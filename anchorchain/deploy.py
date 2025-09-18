from web3 import Web3
import json
import os
import time
from solcx import compile_source, install_solc

def deploy_contract():
    """Deploy AnchorChain contract and save deployment info"""
    
    # Configuration
    rpc_url = os.getenv("RPC_URL", "http://anvil:8545")
    private_key = os.getenv("PRIVATE_KEY", "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
    chain_id = int(os.getenv("CHAIN_ID", "31337"))
    
    print(f"Deploying to {rpc_url} (Chain ID: {chain_id})")
    
    # Wait for blockchain to be ready
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    for i in range(30):
        try:
            if w3.is_connected():
                print("✓ Blockchain connection established")
                break
        except:
            pass
        print(f"Waiting for blockchain... ({i+1}/30)")
        time.sleep(2)
    else:
        raise Exception("Failed to connect to blockchain")
    
    # Install solc
    try:
        install_solc('0.8.19')
    except:
        print("Using existing solc installation")
    
    # Read and compile contract
    with open('contracts/AnchorChain.sol', 'r') as f:
        contract_source = f.read()
    
    compiled = compile_source(contract_source, output_values=['abi', 'bin'])
    contract_interface = compiled['<stdin>:AnchorChain']
    
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']
    
    # Deploy contract
    account = w3.eth.account.from_key(private_key)
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Build transaction
    transaction = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'chainId': chain_id
    })
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    print(f"Transaction sent: {tx_hash.hex()}")
    
    # Wait for confirmation
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = receipt.contractAddress
    
    print(f"✓ Contract deployed at: {contract_address}")
    
    # Save deployment info
    deployment_info = {
        "contract_address": contract_address,
        "abi": abi,
        "tx_hash": tx_hash.hex(),
        "block_number": receipt.blockNumber,
        "chain_id": chain_id,
        "rpc_url": rpc_url
    }
    
    # Write to shared volume
    os.makedirs("/shared/anchor", exist_ok=True)
    with open("/shared/anchor/deployment.json", "w") as f:
        json.dump(deployment_info, f, indent=2)
    
    print("✓ Deployment info saved to /shared/anchor/deployment.json")
    return deployment_info

if __name__ == "__main__":
    try:
        deploy_contract()
        print("🚀 Deployment completed successfully!")
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        exit(1)
