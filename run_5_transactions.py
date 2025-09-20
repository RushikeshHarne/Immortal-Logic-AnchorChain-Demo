#!/usr/bin/env python3
import requests
import time
import hashlib

def generate_soul_hash(entity_id: str) -> str:
    timestamp = str(int(time.time()))
    data = f"{entity_id}:{timestamp}"
    hash_bytes = hashlib.sha256(data.encode()).digest()
    return "0x" + hash_bytes.hex()

def run_transaction(tx_num: int):
    soul_hash = generate_soul_hash(f"entity-{tx_num}")
    payload = {"soul_hash": soul_hash}
    
    print(f"🔗 Transaction #{tx_num}: {soul_hash[:18]}...")
    
    try:
        response = requests.post("http://localhost:8000/notarize", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Transaction #{tx_num} successful: {result.get('tx_hash', 'N/A')}")
            return True
        else:
            print(f"❌ Transaction #{tx_num} failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Transaction #{tx_num} error: {e}")
        return False

def main():
    print("🚀 Running 5 AnchorChain Transactions...")
    
    successful = 0
    for i in range(1, 6):
        if run_transaction(i):
            successful += 1
        time.sleep(1)  # Brief pause between transactions
    
    print(f"\n📊 Results: {successful}/5 transactions successful")

if __name__ == "__main__":
    main()
