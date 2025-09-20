#!/usr/bin/env python3
import requests
import hashlib
import time

def generate_proper_hash():
    """Generate hash in correct format for contract"""
    data = f"test_{int(time.time())}"
    hash_bytes = hashlib.sha256(data.encode()).digest()
    return hash_bytes.hex()  # 64 char hex string

def test_with_proper_format():
    soul_hash = generate_proper_hash()
    print(f"Testing with proper hash: {soul_hash}")
    
    try:
        response = requests.post(f"http://localhost:8000/notarize/{soul_hash}")
        print(f"Response: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print(f"Success: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_with_proper_format()
