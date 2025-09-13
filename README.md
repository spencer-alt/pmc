# Polymarket Local Execution Package

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
