import json
import config
import soupManager as Sm
import jsTrigger
from utils import log

def get_best_coin_logic():
    """Analyzes the market and selects the most profitable coin."""
    if config.state.miner_paused:
        return None, []

    urls = []
    coins = []
    
    # 1. Loading wallet and link configurations
    try:
        with open(config.PATH_WALLETS, 'r') as file:
            wallets = json.load(file)
        with open(config.PATH_POOLS, 'r') as file:
            pools = json.load(file)
        with open(config.PATH_LINKS, 'r') as f:
            for line in f:
                if line.strip(): 
                    urls.append(line.strip())
    except FileNotFoundError as e:
        log(f"[ERROR] Missing configuration file: {e}", force=True)
        return None, []

    # 2. Scraping data from web pages
    log(f"[INFO] Analyzing {len(urls)} links...")
    try:
        # jsTrigger handles JavaScript rendering
        results = jsTrigger.process_urls(urls)
    except Exception as e:
        log(f"[ERROR] Error in jsTrigger: {e}", force=True)
        return None, []
    
    # 3. Processing and filtering results
    for url, content in results.items():
        try:
            # Calculate income based on your hashrate of 17.3 kH/s
            coin_data = Sm.SoupManagerCoin(content, config.MY_HASHRATE_KH).getInformation()
            
            raw_name = coin_data.get("Coin name", "")
            if not raw_name: 
                continue
            
            # Take the first part of the name as the key (e.g., "Monero")
            coin_key = raw_name.split()[0]
            
            # Check if we have a wallet and pool for this coin
            if coin_key in wallets and coin_key in pools:
                coin_data['Wallet'] = wallets[coin_key]
                coin_data['Pool'] = pools[coin_key]
                coin_data['Key'] = coin_key 
                coins.append(coin_data)
                log(f" -> Candidate: {coin_key} (${coin_data.get('Income per day in usd', 0):.2f})")
        except Exception as e:
            log(f"[WARN] Error parsing data for {url}: {e}")

    # 4. Sorting and selecting the best offer
    if not coins:
        log("[WARN] No matching coins found in JSON files.")
        return None, []
        
    # Sort by income in descending order
    coins = sorted(coins, key=lambda x: x.get("Income per day in usd", 0), reverse=True)
    best_one = coins[0]
    
    log(f"[INFO] ==> BEST OPTION: {best_one['Key']} (${best_one.get('Income per day in usd', 0):.2f}/day)")
    return best_one, coins