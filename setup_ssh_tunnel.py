#!/usr/bin/env python3
"""
SSH Tunnel Setup Script for Polymarket Copy Trading Bot

This script helps establish an SSH tunnel from Devin's environment to the user's machine
to route API calls through the user's IP address, bypassing Cloudflare geographic restrictions.

Usage:
1. User sets up SSH access on their machine
2. User runs this script to establish the tunnel
3. Bot uses the tunnel for order posting API calls
"""

import subprocess
import time
import requests
import os
import signal
import sys
from typing import Optional

class SSHTunnel:
    def __init__(self, user_host: str, local_port: int = 8080, remote_host: str = "clob.polymarket.com", remote_port: int = 443):
        self.user_host = user_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.tunnel_process: Optional[subprocess.Popen] = None
        
    def setup_tunnel(self):
        """Establish SSH tunnel to user's machine"""
        print(f"Setting up SSH tunnel to {self.user_host}...")
        print(f"Local port: {self.local_port}")
        print(f"Remote: {self.remote_host}:{self.remote_port}")
        
        ssh_cmd = [
            "ssh",
            "-L", f"{self.local_port}:{self.remote_host}:{self.remote_port}",
            "-N",  # Don't execute remote command
            "-T",  # Disable pseudo-terminal allocation
            self.user_host
        ]
        
        try:
            self.tunnel_process = subprocess.Popen(
                ssh_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(3)
            
            if self.tunnel_process.poll() is None:
                print("✓ SSH tunnel established successfully")
                return True
            else:
                stdout, stderr = self.tunnel_process.communicate()
                print(f"✗ SSH tunnel failed: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"✗ Error setting up SSH tunnel: {e}")
            return False
    
    def test_tunnel(self):
        """Test if the tunnel is working by making a test API call"""
        print("Testing tunnel connectivity...")
        
        try:
            response = requests.get(f"http://localhost:{self.local_port}/markets", timeout=10)
            if response.status_code == 200:
                print("✓ Tunnel test successful - API accessible through tunnel")
                return True
            else:
                print(f"✗ Tunnel test failed - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Tunnel test failed: {e}")
            return False
    
    def close_tunnel(self):
        """Close the SSH tunnel"""
        if self.tunnel_process:
            print("Closing SSH tunnel...")
            self.tunnel_process.terminate()
            self.tunnel_process.wait()
            print("✓ SSH tunnel closed")
    
    def monitor_tunnel(self):
        """Monitor tunnel health and reconnect if needed"""
        print("Monitoring tunnel health (Ctrl+C to stop)...")
        
        def signal_handler(sig, frame):
            print("\nShutting down tunnel...")
            self.close_tunnel()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        while True:
            if self.tunnel_process and self.tunnel_process.poll() is not None:
                print("⚠ Tunnel disconnected, attempting to reconnect...")
                if self.setup_tunnel():
                    print("✓ Tunnel reconnected")
                else:
                    print("✗ Failed to reconnect tunnel")
                    break
            
            if not self.test_tunnel():
                print("⚠ Tunnel connectivity test failed")
            
            time.sleep(30)

def main():
    print("=== Polymarket Bot SSH Tunnel Setup ===")
    print()
    print("This script establishes an SSH tunnel to route API calls through your IP address.")
    print("Prerequisites:")
    print("1. SSH server running on your machine")
    print("2. SSH key authentication set up")
    print("3. Firewall allows SSH connections")
    print()
    
    user_host = input("Enter your machine's SSH address (user@hostname or user@ip): ").strip()
    if not user_host:
        print("Error: SSH address is required")
        return
    
    print(f"Testing SSH connectivity to {user_host}...")
    test_cmd = ["ssh", "-o", "ConnectTimeout=10", user_host, "echo 'SSH connection successful'"]
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print("✓ SSH connection successful")
        else:
            print(f"✗ SSH connection failed: {result.stderr}")
            print("Please ensure:")
            print("- SSH server is running on your machine")
            print("- SSH key authentication is set up")
            print("- Firewall allows SSH connections")
            return
    except Exception as e:
        print(f"✗ SSH test failed: {e}")
        return
    
    tunnel = SSHTunnel(user_host)
    
    if tunnel.setup_tunnel():
        if tunnel.test_tunnel():
            print()
            print("🎉 SSH tunnel is ready!")
            print(f"Bot will route API calls through localhost:{tunnel.local_port}")
            print()
            print("You can now run the bot with tunnel support enabled.")
            print("The tunnel will remain active until you stop this script.")
            print()
            
            tunnel.monitor_tunnel()
        else:
            print("✗ Tunnel test failed")
            tunnel.close_tunnel()
    else:
        print("✗ Failed to establish tunnel")

if __name__ == "__main__":
    main()
