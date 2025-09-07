#!/usr/bin/env python3
import requests
import time
import threading

def send_requests(endpoint, duration, rate):
    """Send requests at specified rate for given duration"""
    end_time = time.time() + duration
    count = 0
    
    while time.time() < end_time:
        try:
            requests.get(endpoint, timeout=2)
            count += 1
            print(f"Sent request {count}")
        except:
            print("Request failed")
        time.sleep(1/rate)  # Control request rate

def create_load_pattern(base_url="http://localhost:8080"):
    endpoint = f"{base_url}/metrics"
    
    print("Starting load pattern...")
    
    # Pattern: Low -> High -> Low -> High
    patterns = [
        (10, 1),   # 10 seconds at 1 req/sec (low)
        (15, 5),   # 15 seconds at 5 req/sec (high)
        (10, 1),   # 10 seconds at 1 req/sec (low)
        (15, 8),   # 15 seconds at 8 req/sec (very high)
        (10, 0.5), # 10 seconds at 0.5 req/sec (very low)
    ]
    
    for duration, rate in patterns:
        print(f"Phase: {rate} req/sec for {duration}s")
        send_requests(endpoint, duration, rate)
        time.sleep(2)  # Brief pause between phases

if __name__ == "__main__":
    create_load_pattern()
