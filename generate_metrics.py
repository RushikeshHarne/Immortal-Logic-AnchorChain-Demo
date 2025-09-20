#!/usr/bin/env python3
import requests
import hashlib
import time

def generate_soul_hash():
    data = f"test_{int(time.time())}"
    return hashlib.sha256(data.encode()).hexdigest()

def test_transaction():
    soul_hash = generate_soul_hash()
    print(f"Testing with hash: {soul_hash}")
    
    try:
        response = requests.post(f"http://localhost:8000/notarize/{soul_hash}")
        print(f"Response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Generating test transactions for metrics...")
    for i in range(3):
        print(f"\nTransaction {i+1}:")
        test_transaction()
        time.sleep(1)
