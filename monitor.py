import requests
import os
from datetime import datetime
import pandas as pd

def send_telegram_alert(ratio):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_ID')
    message = f"🚨 Hive Reward Chance! Ratio: {ratio:.4f} at {datetime.now()}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

def get_pool_stats():
    url = "https://api.hive-engine.com/rpc/contracts"
    payload = {"jsonrpc":"2.0","method":"find","params":{"contract":"market","table":"pools","query":{"symbol":"SWAP.HIVE"}},"id":1}
    response = requests.post(url, json=payload).json()
    pool = response['result'][0]
    hive_balance = float(pool['tokenBalance'])
    swap_balance = float(pool['baseBalance'])
    ratio = hive_balance / swap_balance
    return ratio

if __name__ == "__main__":
    ratio = get_pool_stats()
    if ratio is not None:
        if ratio < 0.95 or ratio > 1.05:
            send_telegram_alert(ratio)
