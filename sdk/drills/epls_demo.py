#!/usr/bin/env python3

import requests
import json
import time
import argparse

def test_api(base_url="http://localhost:8000", token="demo-token-123"):
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Testing AnchorChain API at {base_url}")
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(f"{base_url}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test metrics endpoint
    print("\n2. Testing metrics endpoint...")
    response = requests.get(f"{base_url}/metrics")
    print(f"Status: {response.status_code}")
    print("Metrics preview:")
    for line in response.text.split('\n')[:10]:
        if 'anchorchain' in line:
            print(f"  {line}")
    
    # Test anchor endpoint
    print("\n3. Testing anchor endpoint...")
    anchor_data = {
        "soul_id": "test-soul-001",
        "state_hash": "0x1234567890abcdef"
    }
    
    response = requests.post(
        f"{base_url}/anchor",
        json=anchor_data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success! TX Hash: {result['tx_hash']}")
        print(f"Block Number: {result['block_number']}")
    else:
        print(f"Error: {response.text}")
    
    # Check metrics again
    print("\n4. Checking updated metrics...")
    time.sleep(2)
    response = requests.get(f"{base_url}/metrics")
    for line in response.text.split('\n'):
        if 'anchorchain_tx' in line and not line.startswith('#'):
            print(f"  {line}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test AnchorChain API')
    parser.add_argument('--mode', choices=['local', 'testnet'], default='local')
    parser.add_argument('--url', default='http://localhost:8000')
    parser.add_argument('--token', default='demo-token-123')
    
    args = parser.parse_args()
    
    print(f"Running in {args.mode} mode")
    test_api(args.url, args.token)
