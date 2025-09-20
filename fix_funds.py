#!/usr/bin/env python3
import os
import subprocess

def switch_to_local():
    """Switch to local Ganache for testing"""
    print("🔄 Switching to local Ganache mode...")
    
    # Stop current containers
    subprocess.run(["docker", "compose", "down"], cwd="/home/ubuntu/test/immortal-logic")
    
    # Start local profile
    subprocess.run(["docker", "compose", "--profile", "local", "up", "-d", "--build"], 
                  cwd="/home/ubuntu/test/immortal-logic")
    
    print("✅ Local mode started - funded accounts available")
    print("🔗 Test endpoint: http://localhost:8000")

if __name__ == "__main__":
    switch_to_local()
