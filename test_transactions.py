#!/usr/bin/env python3
import requests
import time
import json

def test_transactions():
    """Send test transactions and monitor in Grafana"""
    base_url = "http://localhost:8001"
    
    print("🔥 Starting transaction tests...")
    
    for i in range(5):
        try:
            # POST transaction
            response = requests.post(f"{base_url}/", 
                                   json={"tx_id": f"tx_{i}", "amount": 100 + i})
            print(f"TX {i}: Status {response.status_code}")
            
            # GET health check
            requests.get(f"{base_url}/health")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("✅ Test complete! Check Grafana at http://localhost:3000")

if __name__ == "__main__":
    test_transactions()
