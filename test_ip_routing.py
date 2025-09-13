#!/usr/bin/env python3
"""
Test script to verify IP routing solution works for Polymarket API calls
"""

import sys
sys.path.append('.')
import nice_funcs as n
import requests
import os
from dotenv import load_dotenv

def test_direct_connection():
    """Test direct API connection (should fail with 403)"""
    print("=== Testing Direct API Connection ===")
    
    try:
        response = requests.get("https://clob.polymarket.com/markets", timeout=10)
        print(f"GET /markets: {response.status_code}")
        
        response = requests.post("https://clob.polymarket.com/order", json={"test": "data"}, timeout=10)
        print(f"POST /order: {response.status_code}")
        
        if response.status_code == 403:
            print("✓ Confirmed: Direct connection blocked by Cloudflare")
            return False
        else:
            print("⚠ Unexpected: Direct connection not blocked")
            return True
            
    except Exception as e:
        print(f"✗ Direct connection test failed: {e}")
        return False

def test_tunnel_connection():
    """Test API connection through SSH tunnel"""
    print("\n=== Testing SSH Tunnel Connection ===")
    
    try:
        response = requests.get("http://localhost:8080/markets", timeout=10)
        print(f"GET /markets (tunnel): {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Tunnel GET request successful")
            
            response = requests.post("http://localhost:8080/order", json={"test": "data"}, timeout=10)
            print(f"POST /order (tunnel): {response.status_code}")
            
            if response.status_code != 403:
                print("✓ Tunnel bypasses Cloudflare blocking!")
                return True
            else:
                print("✗ Tunnel still blocked by Cloudflare")
                return False
        else:
            print("✗ Tunnel GET request failed")
            return False
            
    except Exception as e:
        print(f"✗ Tunnel connection test failed: {e}")
        print("Make sure SSH tunnel is established: python setup_ssh_tunnel.py")
        return False

def test_clob_client_direct():
    """Test CLOB client with direct connection"""
    print("\n=== Testing CLOB Client (Direct) ===")
    
    try:
        user_address = '0x90e9bF6c345B68eE9fd8D4ECFAddb7Ee4F14c8f4'
        client = n.create_clob_client(user_address, use_tunnel=False)
        print("✓ CLOB client created (direct)")
        
        markets = client.get_markets()
        print(f"✓ Markets retrieved: {len(markets)} markets")
        
        from py_clob_client.clob_types import OrderArgs, OrderType
        
        order_args = OrderArgs(
            token_id="36154994650940048409025465583431998499580993695908461126823705526310399761809",
            price=0.28,
            size=17.86,
            side="BUY"
        )
        
        signed_order = client.create_order(order_args)
        print("✓ Order creation successful")
        
        try:
            resp = client.post_order(signed_order, OrderType.GTC)
            print("✓ Order posted successfully (unexpected!)")
            return True
        except Exception as e:
            if "403" in str(e):
                print("✓ Order posting blocked as expected (403)")
                return False
            else:
                print(f"✗ Unexpected error: {e}")
                return False
                
    except Exception as e:
        print(f"✗ CLOB client test failed: {e}")
        return False

def test_clob_client_tunnel():
    """Test CLOB client with SSH tunnel"""
    print("\n=== Testing CLOB Client (Tunnel) ===")
    
    try:
        user_address = '0x90e9bF6c345B68eE9fd8D4ECFAddb7Ee4F14c8f4'
        client = n.create_clob_client(user_address, use_tunnel=True)
        print("✓ CLOB client created (tunnel)")
        
        markets = client.get_markets()
        print(f"✓ Markets retrieved: {len(markets)} markets")
        
        from py_clob_client.clob_types import OrderArgs, OrderType
        
        order_args = OrderArgs(
            token_id="36154994650940048409025465583431998499580993695908461126823705526310399761809",
            price=0.28,
            size=17.86,
            side="BUY"
        )
        
        signed_order = client.create_order(order_args)
        print("✓ Order creation successful")
        
        try:
            resp = client.post_order(signed_order, OrderType.GTC)
            print("🎉 ORDER POSTED SUCCESSFULLY THROUGH TUNNEL!")
            print(f"Response: {resp}")
            return True
        except Exception as e:
            if "403" in str(e):
                print("✗ Order posting still blocked (tunnel not working)")
                return False
            else:
                print(f"✗ Order posting failed: {e}")
                return False
                
    except Exception as e:
        print(f"✗ CLOB client tunnel test failed: {e}")
        print("Make sure SSH tunnel is established: python setup_ssh_tunnel.py")
        return False

def main():
    load_dotenv()
    
    print("=== IP Routing Test Suite ===")
    print("Testing different connection methods for Polymarket API")
    print()
    
    direct_works = test_direct_connection()
    
    tunnel_works = test_tunnel_connection()
    
    clob_direct_works = test_clob_client_direct()
    
    clob_tunnel_works = test_clob_client_tunnel()
    
    print("\n=== Test Results Summary ===")
    print(f"Direct API connection: {'✓ Works' if direct_works else '✗ Blocked (expected)'}")
    print(f"Tunnel API connection: {'✓ Works' if tunnel_works else '✗ Failed'}")
    print(f"CLOB client direct: {'✓ Works' if clob_direct_works else '✗ Blocked (expected)'}")
    print(f"CLOB client tunnel: {'✓ Works' if clob_tunnel_works else '✗ Failed'}")
    
    if tunnel_works and clob_tunnel_works:
        print("\n🎉 IP routing solution is working!")
        print("You can now run the bot with: USE_SSH_TUNNEL=true python main.py")
    elif not tunnel_works:
        print("\n⚠ SSH tunnel not detected or not working")
        print("Set up tunnel first: python setup_ssh_tunnel.py")
    else:
        print("\n❌ IP routing solution needs debugging")

if __name__ == "__main__":
    main()
