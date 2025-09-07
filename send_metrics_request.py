#!/usr/bin/env python3
import requests
import json
import time
import random

def send_anchor_requests(base_url="http://localhost:8000", count=10):
    """Send anchor requests to generate metrics for Grafana"""
    
    for i in range(count):
        # Generate sample data
        soul_id = f"soul_{random.randint(1000, 9999)}"
        state_hash = f"0x{random.randint(100000, 999999):x}"
        
        payload = {
            "soul_id": soul_id,
            "state_hash": state_hash,
            "timestamp": int(time.time())
        }
        
        try:
            response = requests.post(
                f"{base_url}/anchor",
                json=payload,
                headers={"Authorization": "Bearer demo-token-123"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Request {i+1}: TX {result['tx_hash'][:10]}... Block {result['block_number']}")
            else:
                print(f"❌ Request {i+1}: Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request {i+1}: Error - {e}")
        
        time.sleep(0.5)

def get_metrics(base_url="http://localhost:8000"):
    """Fetch current metrics"""
    try:
        response = requests.get(f"{base_url}/metrics", timeout=5)
        if response.status_code == 200:
            print("\n📊 Current Metrics:")
            print(response.text)
        else:
            print(f"❌ Failed to get metrics: {response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching metrics: {e}")

if __name__ == "__main__":
    print("🚀 Sending requests to generate Grafana metrics...")
    send_anchor_requests()
    get_metrics()
