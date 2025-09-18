#!/usr/bin/env python3
import time
import json
import requests
from prometheus_client import Counter, Histogram, start_http_server

# Prometheus metrics
tx_counter = Counter('blockchain_transactions_total', 'Total transactions', ['status', 'type'])
tx_duration = Histogram('transaction_duration_seconds', 'Transaction processing time')

class TransactionMonitor:
    def __init__(self):
        self.amoy_rpc = "https://rpc-amoy.polygon.technology"
        
    def simulate_transaction(self, tx_type="transfer"):
        """Simulate transaction and emit metrics"""
        start_time = time.time()
        
        try:
            # Simulate transaction call
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            }
            
            response = requests.post(self.amoy_rpc, json=payload, timeout=10)
            
            if response.status_code == 200:
                tx_counter.labels(status='success', type=tx_type).inc()
                print(f"✅ {tx_type} transaction simulated - Block: {response.json()['result']}")
            else:
                tx_counter.labels(status='failed', type=tx_type).inc()
                print(f"❌ {tx_type} transaction failed")
                
        except Exception as e:
            tx_counter.labels(status='error', type=tx_type).inc()
            print(f"🔥 Error: {e}")
        
        duration = time.time() - start_time
        tx_duration.observe(duration)

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8000)
    print("📊 Metrics server started on :8000")
    
    monitor = TransactionMonitor()
    
    # Simulate transactions every 30 seconds
    while True:
        monitor.simulate_transaction("resurrection")
        time.sleep(30)
        monitor.simulate_transaction("notarization") 
        time.sleep(30)
