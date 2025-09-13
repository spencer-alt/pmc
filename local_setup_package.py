#!/usr/bin/env python3
"""
Complete local setup package for Polymarket copy trading bot
This creates everything needed to run the local execution component
"""

import os
import json

def create_local_package():
    """Create a complete local package with all necessary files"""
    
    env_template = """# Polymarket API Credentials
WPK=your_private_key_here
WPK_CLOB_API_KEY=3141b78a-f1d9-5a39-4f9d-199d679ec6fb
WPK_CLOB_SECRET=FzR2zUwXW-fxBCjwHVhuHiL73JS87zPOm2kQ0E5SWoA=
WPK_CLOB_PASS_PHRASE=ece5a40c1196157668d252fcf31d5c535ee6f2b0c460f46f14489a140b537418

PROXY_WALLET=0x90e9bF6c345B68eE9fd8D4ECFAddb7Ee4F14c8f4
"""

    requirements = """py-clob-client==0.3.0
python-dotenv==1.0.0
requests==2.31.0
"""

    setup_script = """#!/usr/bin/env python3
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
    if run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("✓ Dependencies installed successfully")
    else:
        print("✗ Failed to install dependencies")
        return False
    
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
"""

    local_executor = """#!/usr/bin/env python3
'''
Local Trade Executor for Polymarket Copy Trading Bot
Executes trades locally using your IP address to bypass geographic restrictions
'''

import json
import time
import os
import sys
from typing import Dict, List
from dotenv import load_dotenv

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType, ApiCreds
from py_clob_client.constants import POLYGON

def create_clob_client(funder_address: str) -> ClobClient:
    '''Create CLOB client for local execution'''
    load_dotenv()
    
    host = "https://clob.polymarket.com"
    private_key = os.getenv("WPK")
    
    if not private_key:
        raise ValueError("WPK (private key) not found in .env file")
    
    creds = ApiCreds(
        api_key=os.getenv("WPK_CLOB_API_KEY"),
        api_secret=os.getenv("WPK_CLOB_SECRET"),
        api_passphrase=os.getenv("WPK_CLOB_PASS_PHRASE"),
    )
    
    client = ClobClient(
        host=host,
        key=private_key,
        creds=creds,
        chain_id=POLYGON,
        signature_type=2,
        funder=funder_address
    )
    
    return client

class LocalTradeExecutor:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.client = None
        self.processed_trades = set()
        
    def setup_client(self):
        '''Initialize CLOB client for local execution'''
        try:
            self.client = create_clob_client(self.wallet_address)
            print(f"✓ CLOB client initialized for wallet: {self.wallet_address}")
            
            markets = self.client.get_markets()
            print(f"✓ API connection verified: {len(markets)} markets available")
            return True
            
        except Exception as e:
            print(f"✗ Failed to initialize CLOB client: {e}")
            return False
    
    def get_pending_trades(self, trades_file: str = "tail_trades.json") -> List[Dict]:
        '''Get trades that need to be executed'''
        try:
            if not os.path.exists(trades_file):
                print(f"Trades file {trades_file} not found. Waiting for trades...")
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
        '''Execute a single trade locally'''
        try:
            print(f"\\n--- Executing Trade ---")
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
        '''Mark trade as executed in the trades file'''
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
        '''Main execution loop'''
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
            print("\\nShutting down local executor...")

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
"""

    readme = """# Polymarket Local Execution Package

This package allows you to run the trade execution component of the Polymarket copy trading bot locally on your machine, bypassing geographic restrictions.


1. **Install Python 3.11+** (recommended for compatibility)

2. **Run setup script:**
   ```bash
   python setup.py
   ```

3. **Configure environment:**
   - Copy `.env.template` to `.env`
   - Add your private key to the `WPK` field in `.env`

4. **Run the executor:**
   ```bash
   python local_executor.py
   ```


- **Monitors** for new trades from the main bot (running in Devin's environment)
- **Executes** BUY trades only for a flat $5 amount
- **Uses your IP address** to bypass Cloudflare geographic restrictions
- **Marks trades as completed** to prevent duplicates


- `setup.py` - One-time setup script
- `local_executor.py` - Main execution script
- `requirements.txt` - Python dependencies
- `.env.template` - Environment configuration template
- `README.md` - This file


- Make sure you're using Python 3.11+
- Run `python setup.py` to verify all dependencies are installed

- Check your internet connection
- Verify your .env file has the correct API credentials
- Make sure your private key (WPK) is set correctly

- The trades file (`tail_trades.json`) is created by the main bot
- Make sure the main bot is running and detecting trades
- Check that the file path is correct when prompted


If you encounter issues:
1. Run `python setup.py` to verify your environment
2. Check that all credentials are correctly set in `.env`
3. Ensure you're using Python 3.11 or newer
"""

    files_to_create = {
        '.env.template': env_template,
        'requirements.txt': requirements,
        'setup.py': setup_script,
        'local_executor.py': local_executor,
        'README.md': readme
    }
    
    print("Creating local package files...")
    for filename, content in files_to_create.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✓ Created {filename}")
    
    print("\nLocal package created successfully!")
    print("Files created:")
    for filename in files_to_create.keys():
        print(f"  - {filename}")

if __name__ == "__main__":
    create_local_package()
