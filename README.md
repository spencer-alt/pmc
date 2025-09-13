# polymarket_copy_trader
An automated bot for copying BUY trades from a leader wallet on Polymarket

- **Simplified Usage**: Bot copies all BUY trades for a flat $5 amount
- **Geographic Fix**: Includes IP routing solution to bypass Cloudflare restrictions
- **Leader Wallet**: Monitors `0x88712ac5d0f65592fcccb4708523c8fa6ee5830a`

## IP Routing Solutions

Due to geographic restrictions, the bot may encounter Cloudflare 403 errors when posting orders. Two solutions are provided:

### Option 1: SSH Tunnel (Recommended)
1. **Set up SSH access on your machine:**
   - Enable SSH server: `sudo systemctl enable ssh && sudo systemctl start ssh`
   - Configure SSH key authentication (recommended)
   - Note your machine's IP address or hostname

2. **Run the tunnel setup script:**
   ```bash
   python setup_ssh_tunnel.py
   ```
   - Enter your SSH address when prompted (e.g., `user@192.168.1.100`)
   - Script will test connectivity and establish tunnel
   - Keep this script running while bot operates

3. **Run bot with tunnel enabled:**
   ```bash
   USE_SSH_TUNNEL=true python main.py
   ```

### Option 2: Local Execution
1. **Run detection in Devin's environment** (monitors leader wallet)
2. **Run execution locally on your machine:**
   ```bash
   python run_local.py
   ```
3. Trades execute using your IP address, bypassing restrictions

### Troubleshooting
- **SSH Connection Failed**: Check firewall settings, SSH service status
- **Tunnel Test Failed**: Verify SSH tunnel is active, check port 8080
- **403 Errors Persist**: Ensure tunnel is routing correctly, try local execution
- **No Trades Detected**: Check leader wallet activity, verify bot is monitoring correct address

# Project Setup

This guide will help you set up the project environment using the provided `requirements.txt` file.

## Prerequisites

- Python installed on your machine.
- A virtual environment (recommended) to keep dependencies isolated.

## Setting Up Your Environment

### 1. Clone the Repository

Clone the repository to your local machine using:

```bash
git clone https://github.com/Joshbazz/polymarket_copy_trader.git
cd polymarket_copy_trader
```

### 2. Create a Virtual Environment

Create a virtual environment to keep your dependencies isolated:

```bash
python -m venv venv
### This will create a directory named venv in your project folder.
```
### 3. Activate the Virtual Environment

Activate the virtual environment using the following command:

On Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install the Required Dependencies

Once your virtual environment is activated, install the required dependencies listed in requirements.txt:

``` bash
pip install -r requirements.txt
## This command will install all the packages and their respective versions specified in the requirements.txt file.
```

### 5. Deactivate the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment using:

``` bash
deactivate
```

### Updating Dependencies

If you add new packages or update existing ones, make sure to update the requirements.txt file with:
```bash
pip freeze > requirements.txt
## This will overwrite the old requirements.txt with the current environment's dependencies.
Troubleshooting
```

Virtual Environment Not Activating: Ensure you are using the correct activation command for your operating system.

Permission Errors: If you encounter permission errors while installing packages, ensure your terminal or command prompt has the necessary permissions or try running it as an administrator (Windows) or with sudo (macOS/Linux).

Dependency Conflicts: If dependencies conflict during installation, consider updating your virtual environment or reviewing the required package versions.
