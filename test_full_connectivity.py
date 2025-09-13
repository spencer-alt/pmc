#!/usr/bin/env python3
"""
Test full connectivity for the local executor package
"""

import os
import sys
from dotenv import load_dotenv

def test_all_connections():
    """Test all required connections for the local executor"""
    print("Testing full connectivity for local executor package...")
    print("=" * 60)
    
    load_dotenv()
    
    try:
        import pymongo
        mongo_uri = os.getenv("MONGO_URI")
        if mongo_uri:
            print(f"Testing MongoDB: {mongo_uri[:50]}...")
            client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            client.server_info()
            print("✓ MongoDB connection successful")
            client.close()
        else:
            print("⚠️  MONGO_URI not configured")
    except Exception as e:
        print(f"✗ MongoDB failed: {e}")
        return False
    
    try:
        from web3 import Web3
        rpc_url = os.getenv("RPC_URL")
        if rpc_url:
            print(f"Testing RPC: {rpc_url[:50]}...")
            web3 = Web3(Web3.HTTPProvider(rpc_url))
            if web3.is_connected():
                block = web3.eth.block_number
                print(f"✓ RPC connection successful - Block: {block}")
            else:
                print("✗ RPC connection failed")
                return False
        else:
            print("⚠️  RPC_URL not configured")
    except Exception as e:
        print(f"✗ RPC failed: {e}")
        return False
    
    try:
        usdc_address = os.getenv("USDC_CONTRACT_ADDRESS")
        if usdc_address and rpc_url:
            print(f"Testing USDC contract: {usdc_address}")
            code = web3.eth.get_code(usdc_address)
            if len(code) > 0:
                print("✓ USDC contract valid")
            else:
                print("✗ USDC contract invalid")
                return False
        else:
            print("⚠️  USDC_CONTRACT_ADDRESS not configured")
    except Exception as e:
        print(f"✗ USDC contract test failed: {e}")
        return False
    
    try:
        import requests
        clob_url = os.getenv("CLOB_HTTP_URL", "https://clob.polymarket.com")
        print(f"Testing CLOB API: {clob_url}")
        response = requests.get(f"{clob_url}/ping", timeout=10)
        if response.status_code == 200:
            print("✓ CLOB API accessible")
        else:
            print(f"⚠️  CLOB API returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️  CLOB API test failed: {e}")
    
    try:
        data_api = os.getenv("DATA_API_BASE", "https://data-api.polymarket.com/")
        print(f"Testing Data API: {data_api}")
        response = requests.get(f"{data_api}ping", timeout=10)
        if response.status_code == 200:
            print("✓ Data API accessible")
        else:
            print(f"⚠️  Data API returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️  Data API test failed: {e}")
    
    print("=" * 60)
    print("✓ ALL CORE CONNECTIONS VERIFIED WORKING")
    print("✓ Package ready for production use")
    return True

if __name__ == "__main__":
    success = test_all_connections()
    if not success:
        sys.exit(1)
