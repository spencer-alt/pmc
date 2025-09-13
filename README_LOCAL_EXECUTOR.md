# Polymarket Local Executor

This package allows you to execute Polymarket trades locally using your own IP address, bypassing geographic restrictions.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   python3.11 setup.py
   ```

2. **Configure Environment**
   - Copy `.env.template` to `.env`
   - Add your private key to the `WPK` field
   - Customize other settings as needed:
     - `USER_ADDRESS`: Leader wallet to monitor (default: 0x88712ac5d0f65592fcccb4708523c8fa6ee5830a)
     - `RPC_URL`: Your Polygon RPC endpoint
     - `MONGO_URI`: MongoDB connection string (if using database features)
     - `FETCH_INTERVAL`: Polling interval in seconds (default: 10)

3. **Run the Executor**
   ```bash
   python3.11 local_executor.py
   ```

## Configuration Variables

### Required
- `WPK`: Your wallet private key
- `WPK_CLOB_API_KEY`: Polymarket CLOB API key
- `WPK_CLOB_SECRET`: Polymarket CLOB API secret
- `WPK_CLOB_PASS_PHRASE`: Polymarket CLOB API passphrase

### Optional
- `USER_ADDRESS`: Leader wallet to monitor for trades
- `RPC_URL`: Polygon RPC endpoint for blockchain interactions
- `MONGO_URI`: MongoDB connection string for data storage
- `USDC_CONTRACT_ADDRESS`: USDC token contract address
- `DATA_API_BASE`: Polymarket data API base URL
- `CLOB_HTTP_URL`: CLOB API endpoint
- `CLOB_WS_URL`: CLOB WebSocket endpoint
- `FETCH_INTERVAL`: Polling interval in seconds
- `TOO_OLD_TIMESTAMP`: Maximum trade age in hours
- `RETRY_LIMIT`: Maximum retry attempts for failed operations

## Features

- **Local Execution**: Runs on your machine using your IP address
- **Automatic Wallet Derivation**: Derives wallet address from private key
- **Configurable Polling**: Customizable trade monitoring intervals
- **Environment-Based Configuration**: All settings via environment variables
- **Error Handling**: Robust error handling and retry logic

## Troubleshooting

1. **Import Errors**: Ensure all dependencies are installed with `python3.11 setup.py`
2. **API Errors**: Verify your CLOB API credentials are correct
3. **Connection Issues**: Check your RPC URL and internet connection
4. **Trade Execution Failures**: Ensure sufficient USDC balance in your wallet

## Support

For issues or questions, refer to the main repository documentation or create an issue on GitHub.
