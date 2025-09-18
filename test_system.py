#!/usr/bin/env python3
"""
Test script to verify AnchorChain system functionality
"""
import requests
import json
import time

def test_api_health():
    """Test API health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✓ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_anchor_transaction():
    """Test anchoring a soul state"""
    try:
        payload = {
            "agentId": "agent-001",
            "sourceEmbodimentId": "embodiment-source-1",
            "targetEmbodimentId": "embodiment-target-1",
            "identityHash": "0x1234567890abcdef",
            "missionHash": "0xfedcba0987654321",
            "jurisdiction": "NOVA-1000-ACE"
        }
        
        response = requests.post("http://localhost:8000/anchor", json=payload)
        result = response.json()
        
        if response.status_code == 200:
            print(f"✓ Transaction successful:")
            print(f"  TX Hash: {result['txHash']}")
            print(f"  Block: {result['blockNumber']}")
            print(f"  Cost: {result['costGwei']} Gwei")
            print(f"  Explorer: {result['explorerUrl']}")
            return result['txHash']
        else:
            print(f"❌ Transaction failed: {result}")
            return None
    except Exception as e:
        print(f"❌ Transaction test failed: {e}")
        return None

def test_metrics():
    """Test metrics endpoint"""
    try:
        response = requests.get("http://localhost:8000/metrics")
        if response.status_code == 200:
            print("✓ Metrics endpoint accessible")
            # Show some key metrics
            metrics = response.text
            for line in metrics.split('\n'):
                if 'anchorchain_tx_success_total' in line and not line.startswith('#'):
                    print(f"  {line}")
                elif 'resurrection_verify_pass_total' in line and not line.startswith('#'):
                    print(f"  {line}")
            return True
        else:
            print(f"❌ Metrics endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Metrics test failed: {e}")
        return False

def test_monitoring_stack():
    """Test Prometheus and Grafana"""
    try:
        # Test Prometheus
        prom_response = requests.get("http://localhost:9090/-/healthy")
        if prom_response.status_code == 200:
            print("✓ Prometheus is healthy")
        else:
            print("❌ Prometheus health check failed")
        
        # Test Grafana
        grafana_response = requests.get("http://localhost:3000/api/health")
        if grafana_response.status_code == 200:
            print("✓ Grafana is healthy")
            print("  Access Grafana at: http://localhost:3000 (admin/admin)")
        else:
            print("❌ Grafana health check failed")
            
        return True
    except Exception as e:
        print(f"❌ Monitoring stack test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing AnchorChain System")
    print("=" * 50)
    
    # Wait for services to be ready
    print("Waiting for services to start...")
    time.sleep(10)
    
    # Run tests
    tests = [
        ("API Health", test_api_health),
        ("Anchor Transaction", test_anchor_transaction),
        ("Metrics Endpoint", test_metrics),
        ("Monitoring Stack", test_monitoring_stack)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems operational!")
        print("\nNext steps:")
        print("1. Check Grafana dashboard: http://localhost:3000")
        print("2. Monitor Prometheus: http://localhost:9090")
        print("3. For testnet deployment, configure .env with your keys")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()
