#!/usr/bin/env python3
"""
Test MongoDB and RPC URL connectivity from user's .env configuration
"""

import os
import sys
from dotenv import load_dotenv

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        import pymongo
        
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        
        if not mongo_uri:
            print("✗ MONGO_URI not found in .env")
            return False
            
        print(f"Testing MongoDB connection to: {mongo_uri[:50]}...")
        
        client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✓ MongoDB connection successful")
        client.close()
        return True
        
    except ImportError:
        print("⚠️  pymongo not installed - MongoDB test skipped")
        return None
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

def test_rpc_connection():
    """Test RPC URL connection"""
    try:
        from web3 import Web3
        
        load_dotenv()
        rpc_url = os.getenv("RPC_URL")
        
        if not rpc_url:
            print("✗ RPC_URL not found in .env")
            return False
            
        print(f"Testing RPC connection to: {rpc_url[:50]}...")
        
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if web3.is_connected():
            latest_block = web3.eth.block_number
            print(f"✓ RPC connection successful - Latest block: {latest_block}")
            return True
        else:
            print("✗ RPC connection failed - not connected")
            return False
            
    except ImportError:
        print("⚠️  web3 not installed - RPC test skipped")
        return None
    except Exception as e:
        print(f"✗ RPC connection failed: {e}")
        return False

def test_usdc_contract():
    """Test USDC contract address"""
    try:
        from web3 import Web3
        
        load_dotenv()
        rpc_url = os.getenv("RPC_URL")
        usdc_address = os.getenv("USDC_CONTRACT_ADDRESS")
        
        if not rpc_url or not usdc_address:
            print("✗ RPC_URL or USDC_CONTRACT_ADDRESS not found")
            return False
            
        print(f"Testing USDC contract: {usdc_address}")
        
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not web3.is_connected():
            print("✗ Cannot test USDC contract - RPC not connected")
            return False
            
        code = web3.eth.get_code(usdc_address)
        if len(code) > 0:
            print("✓ USDC contract address valid - has bytecode")
            return True
        else:
            print("✗ USDC contract address invalid - no bytecode")
            return False
            
    except Exception as e:
        print(f"✗ USDC contract test failed: {e}")
        return False

def main():
    print("Testing connectivity for user's configuration...")
    print("=" * 50)
    
    mongo_result = test_mongodb_connection()
    print()
    
    rpc_result = test_rpc_connection()
    print()
    
    usdc_result = test_usdc_contract()
    print()
    
    print("=" * 50)
    print("CONNECTIVITY TEST SUMMARY:")
    
    if mongo_result is True:
        print("✓ MongoDB: WORKING")
    elif mongo_result is False:
        print("✗ MongoDB: FAILED")
    else:
        print("⚠️  MongoDB: SKIPPED (dependency missing)")
        
    if rpc_result is True:
        print("✓ RPC URL: WORKING")
    elif rpc_result is False:
        print("✗ RPC URL: FAILED")
    else:
        print("⚠️  RPC URL: SKIPPED (dependency missing)")
        
    if usdc_result is True:
        print("✓ USDC Contract: VALID")
    elif usdc_result is False:
        print("✗ USDC Contract: INVALID")
    else:
        print("⚠️  USDC Contract: SKIPPED")
    
    working_count = sum(1 for result in [mongo_result, rpc_result, usdc_result] if result is True)
    failed_count = sum(1 for result in [mongo_result, rpc_result, usdc_result] if result is False)
    
    if failed_count > 0:
        print(f"\n⚠️  {failed_count} configuration(s) failed - package may not work correctly")
        return False
    elif working_count > 0:
        print(f"\n✓ All tested configurations working ({working_count} verified)")
        return True
    else:
        print(f"\n⚠️  No configurations could be tested (missing dependencies)")
        return None

if __name__ == "__main__":
    success = main()
    if success is False:
        sys.exit(1)
