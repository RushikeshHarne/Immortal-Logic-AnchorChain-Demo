#!/usr/bin/env python3
import requests
import hashlib
import time
import json

API_BASE = "http://localhost:8000"

def generate_soul_hash():
    """Generate a test soul hash"""
    data = f"soul_{int(time.time())}"
    return hashlib.sha256(data.encode()).hexdigest()

def test_resurrection_flow():
    """Test complete resurrection flow"""
    print("🔥 Starting Immortal Logic Resurrection Drill...")
    
    # Check API status
    response = requests.get(f"{API_BASE}/")
    print(f"API Status: {response.json()}")
    
    # Generate soul hash
    soul_hash = generate_soul_hash()
    print(f"Generated Soul Hash: {soul_hash}")
    
    # Notarize resurrection
    print("📝 Notarizing resurrection...")
    notarize_response = requests.post(f"{API_BASE}/notarize", 
                                    json={"soul_hash": soul_hash})
    
    if notarize_response.status_code == 200:
        result = notarize_response.json()
        print(f"✅ Notarization successful: {result['tx_hash']}")
        print(f"Gas used: {result['gas_used']}")
    else:
        print(f"❌ Notarization failed: {notarize_response.text}")
        return
    
    # Wait a moment
    time.sleep(2)
    
    # Verify resurrection
    print("🔍 Verifying resurrection...")
    verify_response = requests.post(f"{API_BASE}/verify", 
                                  json={"soul_hash": soul_hash})
    
    if verify_response.status_code == 200:
        result = verify_response.json()
        print(f"✅ Verification successful: {result['tx_hash']}")
        print(f"Verified: {result['verified']}")
    else:
        print(f"❌ Verification failed: {verify_response.text}")
    
    print("🎯 Resurrection drill completed!")

if __name__ == "__main__":
    test_resurrection_flow()
