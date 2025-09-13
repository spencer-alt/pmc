#!/usr/bin/env python3
"""
Test script to verify py-clob-client 0.25.0 imports work correctly
"""

def test_imports():
    try:
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import OrderArgs, OrderType, ApiCreds
        from py_clob_client.constants import POLYGON
        from dotenv import load_dotenv
        print("✓ All imports successful with py-clob-client 0.25.0")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
