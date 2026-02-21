import datetime
import json
import config

def log(msg, force=False):
    """Helper function for logging with timestamp, using global state."""
    if config.state.logs_enabled or force:
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {msg}", flush=True)

def save_dashboard_status(coin, profit, profit_coin, symbol):
    """Saves the current mining status to a JSON file for the Dashboard."""
    try:
        current_hashrate = config.MY_HASHRATE_KH * 1000
        data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "coin": coin,
            "profit_usd": profit / current_hashrate if current_hashrate > 0 else 0,
            "profit_coin": profit_coin / current_hashrate if current_hashrate > 0 else 0,
            "worker_name": "miner0",
            "symbol": symbol
        }
        with open('json/status.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log(f"[WARN] Failed to save dashboard status: {e}", force=True)

def save_order_for_slaves(coin):
    try:
        data = {
            "coin": coin,
        }

        path = "json/order.json"
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        log(f"[WARN] Failed to save order: {e}", force=True)