#!/usr/bin/env python3
import requests
import time
import json

def fetch_and_display_grafana_metrics(base_url="http://localhost:8000"):
    """Fetch metrics and display them in Grafana-style format"""
    
    print("📊 IMMORTAL LOGIC - GRAFANA METRICS DASHBOARD")
    print("=" * 50)
    
    # Generate some activity first
    print("🔄 Generating activity...")
    for i in range(10):
        requests.get(f"{base_url}/", timeout=2)
        if i % 3 == 0:  # Some anchor attempts
            requests.post(f"{base_url}/anchor", json={"soul_id": f"soul_{i}"})
        time.sleep(0.1)
    
    # Fetch metrics
    try:
        response = requests.get(f"{base_url}/metrics", timeout=5)
        if response.status_code != 200:
            print(f"❌ Failed to fetch metrics: {response.status_code}")
            return
            
        metrics_text = response.text
        
        # Parse key metrics
        tx_ok = 0
        tx_err = 0
        
        for line in metrics_text.split('\n'):
            if line.startswith('anchorchain_tx_ok_total'):
                tx_ok = float(line.split()[-1])
            elif line.startswith('anchorchain_tx_err_total'):
                tx_err = float(line.split()[-1])
        
        # Display in Grafana dashboard style
        print(f"\n🎯 ANCHORCHAIN TRANSACTION METRICS")
        print(f"   Successful Transactions: {int(tx_ok)}")
        print(f"   Failed Transactions:     {int(tx_err)}")
        print(f"   Total Transactions:      {int(tx_ok + tx_err)}")
        
        if tx_ok + tx_err > 0:
            success_rate = (tx_ok / (tx_ok + tx_err)) * 100
            print(f"   Success Rate:           {success_rate:.1f}%")
        
        print(f"\n📈 PROMETHEUS QUERY EXAMPLES:")
        print(f"   Rate of successful TXs:  rate(anchorchain_tx_ok_total[5m])")
        print(f"   Rate of failed TXs:      rate(anchorchain_tx_err_total[5m])")
        print(f"   Success rate:            anchorchain_tx_ok_total / (anchorchain_tx_ok_total + anchorchain_tx_err_total)")
        
        print(f"\n🔍 RAW METRICS (for Grafana):")
        for line in metrics_text.split('\n'):
            if 'anchorchain_tx' in line and not line.startswith('#'):
                print(f"   {line}")
                
    except Exception as e:
        print(f"❌ Error fetching metrics: {e}")

if __name__ == "__main__":
    fetch_and_display_grafana_metrics()
