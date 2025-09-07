#!/usr/bin/env python3
import requests
import time

def test_metrics_endpoint(base_url="http://localhost:8080", num_requests=10):
    endpoint = f"{base_url}/metrics"
    
    for i in range(1, num_requests + 1):
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"Request {i}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request {i}: Failed - {e}")
        
        time.sleep(0.5)  # Brief delay between requests

if __name__ == "__main__":
    test_metrics_endpoint()
