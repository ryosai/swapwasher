import requests
import os
import pandas as pd
from datetime import datetime

def log_data(ratio):
    try:
        # Load existing data
        df = pd.read_csv('pool_history.csv')
    except FileNotFoundError:
        # Create new file if it doesn't exist
        df = pd.DataFrame(columns=['timestamp', 'ratio'])
    
    # Add new entry
    new_entry = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'ratio': ratio}
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    
    # Keep only the last 7 days of data (optional)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[df['timestamp'] > (datetime.now() - pd.Timedelta(days=7))]
    
    # Save back to CSV
    df.to_csv('pool_history.csv', index=False)

# Call this inside __main__ after getting the ratio
if __name__ == "__main__":
    ratio = get_pool_stats()
    if ratio is not None:
        log_data(ratio)  # <-- Add this line
        if ratio < 0.95 or ratio > 1.05:
            send_telegram_alert(ratio)

# Telegram notification function
def send_telegram_alert(ratio):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_ID')
    
    message = (
        f"🚨 **Hive Swap Reward Opportunity** 🚨\n\n"
        f"**Current Ratio:** `{ratio:.4f}`\n"
        f"**Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
        f"[Convert Now](https://beeswap.dcity.io/convert)"
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.get(url, params=params)

# Fetch Hive pool data
def get_pool_stats():
    url = "https://api.hive-engine.com/rpc/contracts"
    payload = {
        "jsonrpc": "2.0",
        "method": "find",
        "params": {
            "contract": "market",
            "table": "pools",
            "query": {"symbol": "SWAP.HIVE"}
        },
        "id": 1
    }
    
    try:
        response = requests.post(url, json=payload).json()
        pool = response['result'][0]
        hive_balance = float(pool['tokenBalance'])
        swap_balance = float(pool['baseBalance'])
        ratio = hive_balance / swap_balance
        return ratio
    except:
        return None

# Main check
if __name__ == "__main__":
    ratio = get_pool_stats()
    if ratio is not None and (ratio < 0.95 or ratio > 1.05):  # Adjust thresholds
        send_telegram_alert(ratio)
