#!/usr/bin/env python3
"""
Local execution script for Polymarket copy trading bot

This script allows the user to run only the trade execution component locally
while keeping detection and filtering in Devin's environment.

Usage:
1. User runs this script on their local machine
2. Script polls for new trades from a shared file/API
3. Executes trades using user's IP address (bypassing geographic restrictions)
"""

import json
import time
import os
import sys
from typing import Dict, List
import requests
from dotenv import load_dotenv

sys.path.append('.')

try:
    import nice_funcs as n
    from py_clob_client.clob_types import OrderArgs, OrderType
except ImportError:
    print("Error: Required dependencies not found.")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

class LocalTradeExecutor:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.client = None
        self.processed_trades = set()
        
    def setup_client(self):
        """Initialize CLOB client for local execution"""
        try:
            self.client = n.create_clob_client(self.wallet_address, use_tunnel=False)
            print(f"✓ CLOB client initialized for wallet: {self.wallet_address}")
            
            markets = self.client.get_markets()
            print(f"✓ API connection verified: {len(markets)} markets available")
            return True
            
        except Exception as e:
            print(f"✗ Failed to initialize CLOB client: {e}")
            return False
    
    def get_pending_trades(self, trades_file: str = "tail_trades.json") -> List[Dict]:
        """Get trades that need to be executed"""
        try:
            if not os.path.exists(trades_file):
                return []
                
            with open(trades_file, 'r') as f:
                trades = json.load(f)
            
            pending = []
            for trade in trades:
                trade_id = trade.get('transactionHash', str(trade.get('timestamp', '')))
                if not trade.get('bot_executed', False) and trade_id not in self.processed_trades:
                    pending.append(trade)
            
            return pending
            
        except Exception as e:
            print(f"Error reading trades file: {e}")
            return []
    
    def execute_trade(self, trade: Dict) -> bool:
        """Execute a single trade locally"""
        try:
            print(f"\n--- Executing Trade ---")
            print(f"Asset: {trade['asset']}")
            print(f"Side: {trade['side']}")
            print(f"Size: $5.00")
            
            price_data = self.client.get_last_trade_price(trade['asset'])
            price = float(price_data['price'])
            size = 5.0 / price  # $5 fixed size
            
            print(f"Price: ${price}")
            print(f"Shares: {size:.2f}")
            
            order_args = OrderArgs(
                token_id=trade['asset'],
                price=price,
                size=size,
                side=trade['side']
            )
            
            signed_order = self.client.create_order(order_args)
            print("✓ Order created and signed")
            
            resp = self.client.post_order(signed_order, OrderType.GTC)
            print(f"✓ Order posted successfully: {resp}")
            
            trade_id = trade.get('transactionHash', str(trade.get('timestamp', '')))
            self.processed_trades.add(trade_id)
            
            return True
            
        except Exception as e:
            print(f"✗ Trade execution failed: {e}")
            return False
    
    def mark_trade_executed(self, trade: Dict, trades_file: str = "tail_trades.json"):
        """Mark trade as executed in the trades file"""
        try:
            with open(trades_file, 'r') as f:
                trades = json.load(f)
            
            trade_id = trade.get('transactionHash', str(trade.get('timestamp', '')))
            for t in trades:
                t_id = t.get('transactionHash', str(t.get('timestamp', '')))
                if t_id == trade_id:
                    t['bot_executed'] = True
                    t['executed_locally'] = True
                    break
            
            with open(trades_file, 'w') as f:
                json.dump(trades, f, indent=4)
                
        except Exception as e:
            print(f"Error updating trades file: {e}")
    
    def run(self, trades_file: str = "tail_trades.json", poll_interval: int = 10):
        """Main execution loop"""
        print("=== Local Trade Executor Started ===")
        print(f"Wallet: {self.wallet_address}")
        print(f"Trades file: {trades_file}")
        print(f"Poll interval: {poll_interval}s")
        print("Press Ctrl+C to stop")
        print()
        
        if not self.setup_client():
            print("Failed to initialize client. Exiting.")
            return
        
        try:
            while True:
                pending_trades = self.get_pending_trades(trades_file)
                
                if pending_trades:
                    print(f"Found {len(pending_trades)} pending trades")
                    
                    for trade in pending_trades:
                        if trade['side'] == 'BUY':  # Only execute BUY trades
                            if self.execute_trade(trade):
                                self.mark_trade_executed(trade, trades_file)
                                print("✓ Trade executed and marked as complete")
                            else:
                                print("✗ Trade execution failed")
                        else:
                            print(f"Skipping SELL trade (BUY only mode)")
                            self.mark_trade_executed(trade, trades_file)
                else:
                    print("No pending trades found")
                
                print(f"Sleeping for {poll_interval} seconds...")
                time.sleep(poll_interval)
                
        except KeyboardInterrupt:
            print("\nShutting down local executor...")

def main():
    load_dotenv()
    
    print("=== Polymarket Local Trade Executor ===")
    print("This script executes trades locally using your IP address")
    print()
    
    wallet_address = os.getenv("PROXY_WALLET", "0x90e9bF6c345B68eE9fd8D4ECFAddb7Ee4F14c8f4")
    print(f"Using wallet: {wallet_address}")
    
    trades_file = input("Enter path to trades file (default: tail_trades.json): ").strip()
    if not trades_file:
        trades_file = "tail_trades.json"
    
    poll_input = input("Enter poll interval in seconds (default: 10): ").strip()
    try:
        poll_interval = int(poll_input) if poll_input else 10
    except ValueError:
        poll_interval = 10
    
    executor = LocalTradeExecutor(wallet_address)
    executor.run(trades_file, poll_interval)

if __name__ == "__main__":
    main()
