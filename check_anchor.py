#!/usr/bin/env python3
import requests
import hashlib
import time

def generate_soul_hash():
    """Generate a proper 32-byte soul hash"""
    data = f"soul_{int(time.time())}"
    return hashlib.sha256(data.encode()).hexdigest()

def check_anchor():
    # Generate soul hash
    soul_hash = generate_soul_hash()
    print(f"Generated Soul Hash: {soul_hash}")
    
    # Test notarize
    print(f"\n📝 Testing notarize endpoint...")
    try:
        response = requests.post(f"http://localhost:8000/notarize/{soul_hash}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Notarize Success: {result['tx_hash']}")
            print(f"Gas Used: {result['gas_used']}")
            return soul_hash
        else:
            print(f"❌ Notarize Failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    soul_hash = check_anchor()
    if soul_hash:
        print(f"\n🔗 Use this hash to verify: {soul_hash}")
        print(f"Verify command: curl -X POST http://localhost:8000/verify/{soul_hash}")
