#!/usr/bin/env python3
"""
Immortal Logic EPLS Demo - End-to-end resurrection drill
"""
import requests
import time
import argparse
import hashlib
import json

def generate_soul_hash(entity_id: str) -> str:
    """Generate a soul state hash"""
    timestamp = str(int(time.time()))
    data = f"{entity_id}:{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()

def test_api_endpoint(base_url: str, token: str):
    """Test the AnchorChain API"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"🔗 Testing AnchorChain API at {base_url}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test metrics endpoint
    try:
        response = requests.get(f"{base_url}/metrics")
        print(f"✅ Metrics endpoint accessible (length: {len(response.text)})")
    except Exception as e:
        print(f"❌ Metrics check failed: {e}")
    
    # Test anchor endpoint
    try:
        soul_hash = generate_soul_hash("demo-entity-001")
        metadata = f"Demo resurrection event at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        payload = {
            "soul_hash": soul_hash,
            "metadata": metadata
        }
        
        print(f"📡 Anchoring soul state: {soul_hash[:16]}...")
        response = requests.post(f"{base_url}/anchor", json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Anchor successful: {result}")
            return True
        else:
            print(f"❌ Anchor failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Anchor test failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Immortal Logic EPLS Demo")
    parser.add_argument("--mode", choices=["local", "onchain"], default="local",
                       help="Demo mode: local (mock) or onchain (real blockchain)")
    parser.add_argument("--api-url", default="http://localhost:8000",
                       help="AnchorChain API URL")
    parser.add_argument("--token", default="demo-token-123",
                       help="API authentication token")
    
    args = parser.parse_args()
    
    print("🚀 Immortal Logic EPLS Demo Starting...")
    print(f"Mode: {args.mode}")
    print(f"API URL: {args.api_url}")
    
    # Run the test
    success = test_api_endpoint(args.api_url, args.token)
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("📊 Check Grafana dashboard at http://localhost:3000 (admin/admin)")
        print("📈 Check Prometheus at http://localhost:9090")
    else:
        print("\n❌ Demo failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
