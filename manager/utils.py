import datetime
import json
import os
import config

def log(msg, force=False):
    """Helper function for logging with timestamp, using global state."""
    if config.state.logs_enabled or force:
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {msg}", flush=True)

def save_dashboard_status(coin, pool, profit):
    """Saves the current mining status to a JSON file for the Dashboard."""
    try:
        data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "coin": coin,
            "pool": pool,
            "profit_usd": profit/(config.MY_HASHRATE_KH*1000),
            "worker_name": "miner0"
        }
        with open('json/status.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log(f"[WARN] Failed to save dashboard status: {e}", force=True)

def save_order_for_slaves(coin, pool, wallet):
    try:
        data = {
            "coin": coin,
            "pool": pool,
            "wallet": wallet,
        }

        path = os.path.join(config.HOST_JSON_PATH, 'order.json')
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        print(f"[ERROR] Nie udało się zapisać order.json: {e}")