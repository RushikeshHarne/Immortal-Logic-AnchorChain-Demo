#!/usr/bin/env python3
"""
AnchorChain Demo Test Script
Tests the complete AnchorChain flow and shows metrics.
"""

import requests
import time
import json

API_BASE = "http://localhost:8000"
API_TOKEN = "demo-token-123"

def test_api():
    print("🚀 Testing AnchorChain Demo")
    print("=" * 50)
    
    # Test API status
    print("1. Testing API status...")
    response = requests.get(f"{API_BASE}/")
    print(f"   Status: {response.json()}")
    
    # Get initial metrics
    print("\n2. Getting initial metrics...")
    response = requests.get(f"{API_BASE}/metrics")
    metrics_text = response.text
    
    # Extract current counters
    ok_count = 0
    err_count = 0
    for line in metrics_text.split('\n'):
        if line.startswith('anchorchain_tx_ok_total'):
            ok_count = float(line.split()[-1])
        elif line.startswith('anchorchain_tx_err_total'):
            err_count = float(line.split()[-1])
    
    print(f"   Initial OK count: {ok_count}")
    print(f"   Initial ERROR count: {err_count}")
    
    # Test successful anchor
    print("\n3. Testing successful anchor transaction...")
    soul_id = f"demo-soul-{int(time.time())}"
    state_hash = f"0x{hash(soul_id) & 0xffffffffffffffff:016x}"
    
    response = requests.post(
        f"{API_BASE}/anchor",
        params={"soul_id": soul_id, "state_hash": state_hash},
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Success! TX: {result['tx_hash']}")
        print(f"   Block: {result['block_number']}")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Get updated metrics
    print("\n4. Getting updated metrics...")
    time.sleep(2)  # Wait for metrics to update
    response = requests.get(f"{API_BASE}/metrics")
    metrics_text = response.text
    
    # Extract updated counters
    new_ok_count = 0
    new_err_count = 0
    for line in metrics_text.split('\n'):
        if line.startswith('anchorchain_tx_ok_total'):
            new_ok_count = float(line.split()[-1])
        elif line.startswith('anchorchain_tx_err_total'):
            new_err_count = float(line.split()[-1])
    
    print(f"   Updated OK count: {new_ok_count} (+{new_ok_count - ok_count})")
    print(f"   Updated ERROR count: {new_err_count} (+{new_err_count - err_count})")
    
    print("\n🎯 Demo URLs:")
    print(f"   API: http://localhost:8000")
    print(f"   Prometheus: http://localhost:9090")
    print(f"   Grafana: http://localhost:3000 (admin/admin)")
    print(f"   Blockchain RPC: http://localhost:8545")
    
    print("\n✅ AnchorChain Demo Test Complete!")

if __name__ == "__main__":
    test_api()
