#!/usr/bin/env python3
import requests
import time

def generate_metrics(base_url="http://localhost:8000"):
    """Generate metrics by making requests to the API"""
    
    print("🚀 Generating metrics for Grafana...")
    
    # Make some successful requests to root endpoint
    for i in range(5):
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            print(f"✅ Health check {i+1}: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check {i+1}: {e}")
        time.sleep(0.2)
    
    # Try anchor requests with minimal data
    anchor_data = {"soul_id": "test_soul", "state_hash": "0x123"}
    
    for i in range(3):
        try:
            response = requests.post(
                f"{base_url}/anchor", 
                json=anchor_data,
                headers={"Authorization": "Bearer demo-token-123"}
            )
            if response.status_code == 200:
                print(f"✅ Anchor {i+1}: Success")
            else:
                print(f"⚠️  Anchor {i+1}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Anchor {i+1}: {e}")
        time.sleep(0.3)
    
    # Fetch and display metrics
    print("\n📊 Current Prometheus Metrics:")
    try:
        response = requests.get(f"{base_url}/metrics")
        if response.status_code == 200:
            # Filter for our custom metrics
            lines = response.text.split('\n')
            for line in lines:
                if 'anchorchain_tx' in line and not line.startswith('#'):
                    print(f"  {line}")
        else:
            print(f"❌ Failed to fetch metrics: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_metrics()
