#!/usr/bin/env python3
import requests
import time

def burst_pattern(endpoint="http://localhost:8080/metrics"):
    # Create visible spikes in Grafana
    for cycle in range(3):
        print(f"Cycle {cycle + 1}: Sending burst...")
        
        # Burst: 20 requests quickly
        for i in range(20):
            try:
                requests.get(endpoint, timeout=1)
            except:
                pass
        
        print("Waiting 30 seconds...")
        time.sleep(30)  # Long pause - creates clear up/down pattern

if __name__ == "__main__":
    burst_pattern()
