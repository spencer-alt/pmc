#!/usr/bin/env python3
'''
Setup script for Polymarket local execution
Run this first to set up your environment
'''

import subprocess
import sys
import os

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {cmd}")
            return True
        else:
            print(f"✗ {cmd}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {cmd}")
        print(f"Error: {e}")
        return False

def main():
    print("=== Polymarket Local Setup ===")
    print("Setting up your local execution environment...")
    print()
    
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major != 3 or python_version.minor < 11:
        print("⚠️  Warning: Python 3.11+ recommended for best compatibility")
    
    print("Installing dependencies...")
    print("Note: This may take a few minutes for first-time installation...")
    
    if run_command(f"{sys.executable} -m pip install --upgrade pip"):
        print("✓ pip upgraded")
    
    if run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("✓ Dependencies installed successfully")
    else:
        print("✗ Failed to install from requirements.txt")
        print("Trying individual package installation...")
        
        packages = [
            "eth-utils>=4.1.1",
            "eth-account>=0.11.0", 
            "pydantic>=2.0.0",
            "py-order-utils>=0.3.2",
            "py-clob-client==0.25.0",
            "python-dotenv>=1.0.0",
            "requests>=2.31.0"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            if not run_command(f"{sys.executable} -m pip install {package}"):
                print(f"✗ Failed to install {package}")
                return False
        
        print("✓ All packages installed individually")
    
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Please create one using .env.template")
        print("   Make sure to add your private key (WPK) to the .env file")
    else:
        print("✓ .env file found")
    
    try:
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import OrderArgs, OrderType, ApiCreds
        from py_clob_client.constants import POLYGON
        from dotenv import load_dotenv
        print("✓ All imports successful")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    print()
    print("=== Setup Complete ===")
    print("Next steps:")
    print("1. Edit .env file with your private key")
    print("2. Run: python local_executor.py")
    print()
    
    return True

if __name__ == "__main__":
    main()
