import config
from utils import log, save_dashboard_status, save_order_for_slaves
from discord_service import send_dm
import json

def read_json(path):
    try:
        with open(f'{path}') as f:
            data = json.load(f)
            return data
    except:
        log(f"[ERROR] opening json file {path}")
        return None

def manage_worker(best_coin, coins):
    new_coin_name = best_coin['Key']
    new_coin_income_usd = best_coin.get('Income per day in usd', 0)
    new_coin_income = best_coin.get("Income per day",0)
    new_coin_symbol = best_coin.get("Symbol",0)

    notification_msg = None
    old_coin_name = None
    try:
        old_coin_name = read_json('json/order.json')['coin']
    except:
        log(f"[ERROR] old_coin_name =  {old_coin_name}")

    old_coin_income_usd = 0
    for c in coins:
        if c.get("Key") == old_coin_name:
            old_coin_income_usd = c.get('Income per day in usd', 0) * config.INCOME_TRESHOLD
            old_coin_income = c.get('Income per day', 0)
            old_coin_symbol = c.get("Symbol", 0)
            break
    if old_coin_name == new_coin_name:
        log(f"[INFO] Staying with {old_coin_name}")
        save_order_for_slaves(old_coin_name)
        save_dashboard_status(old_coin_name, old_coin_income_usd, old_coin_income, old_coin_symbol)
        return
    if old_coin_income_usd >= new_coin_income_usd:
        log(f"[INFO] Staying with {old_coin_name}. Profit increase too small (<{int((config.INCOME_TRESHOLD-1)*100)}%).")
        save_order_for_slaves(old_coin_name)
        save_dashboard_status(old_coin_name, old_coin_income_usd, old_coin_income, old_coin_symbol)
        return

    notification_msg = f"🔄 Miner changed to {new_coin_name}! \nNow one machine is making ${new_coin_income_usd:.2f}/day"
    
    if notification_msg:
        send_dm(notification_msg)
        save_order_for_slaves(new_coin_name)
        save_dashboard_status(new_coin_name, new_coin_income_usd,new_coin_income, new_coin_symbol)

    