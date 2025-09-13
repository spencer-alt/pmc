'''
You can run all three bots in one terminal instance by executing this file.

You can also run every bot separately for easier testing and logic visualization
'''

import multiprocessing
import os
import trade_tailer as trader
import risk_manager
import trade_monitor

user_address = '0x90e9bF6c345B68eE9fd8D4ECFAddb7Ee4F14c8f4'

def run_trade_monitor():
    trade_monitor.main()

def run_trader():
    use_tunnel = os.getenv("USE_SSH_TUNNEL", "false").lower() == "true"
    trader.run_trade_tailer(use_tunnel=use_tunnel)

def run_risk_manager():
    risk_manager.run_risk_manager(user_address)

if __name__ == "__main__":
    print("Starting Polymarket Copy Trading Bot...")
    
    use_tunnel = os.getenv("USE_SSH_TUNNEL", "false").lower() == "true"
    
    if use_tunnel:
        print("SSH Tunnel mode enabled - API calls will route through localhost:8080")
        print("Make sure SSH tunnel is established before running the bot!")
    else:
        print("Direct API mode - may encounter geographic restrictions")
    
    # Create separate processes for each function
    processes = [
        multiprocessing.Process(target=run_trade_monitor),
        multiprocessing.Process(target=run_trader),
        multiprocessing.Process(target=run_risk_manager)
    ]

    # Start each process
    for process in processes:
        process.start()
        
    print("All components started. Bot is running...")
    
    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("\nShutting down bot...")
        for process in processes:
            process.terminate()
