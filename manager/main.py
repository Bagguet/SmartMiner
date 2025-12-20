import docker
import time
import json
import os
import sys
import datetime

try:
    import soupManger as Sm
    import jsTrigger
except ImportError as e:
    print(f"[CRITICAL] Błąd importu: {e}")
    sys.exit(1)

try:
    CLIENT = docker.from_env()
except Exception as e:
    print(f"[ERROR] Nie widzę Dockera. Czy zamontowałeś /var/run/docker.sock? Błąd: {e}")
    sys.exit(1)

CONTAINER_NAME = "active_miner_worker"
IMAGE_NAME = "smartminer_worker_img"
MY_HASHRATE_KH = 16

PATH_WALLETS = 'json/wallets.json'
PATH_POOLS = 'json/pools.json'
PATH_LINKS = 'links.txt' 

def log(msg):
    """Pomocnicze logowanie z datą"""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_best_coin_logic():
    """To jest logika żywcem wyjęta z Twojego bestToMine.py"""
    
    urls = []
    coins = []
    
    # 1. Wczytywanie plików
    try:
        with open(PATH_WALLETS, 'r') as file:
            wallets = json.load(file)
        with open(PATH_POOLS, 'r') as file:
            pools = json.load(file)
        with open(PATH_LINKS, 'r') as f:
            for line in f:
                if line.strip(): urls.append(line.strip())
    except FileNotFoundError as e:
        log(f"[ERROR] Brak pliku: {e} - Sprawdź montowanie wolumenów w docker-compose!")
        return None

    # 2. Webscraping
    log(f"Analizuję {len(urls)} linków...")
    try:
        results = jsTrigger.process_urls(urls)
    except Exception as e:
        log(f"[ERROR] Błąd w jsTrigger: {e}")
        return None
    
    # 3. Przetwarzanie danych
    for url, content in results.items():
        try:
            coin_data = Sm.SoupManagerCoin(content, MY_HASHRATE_KH).getInformation()
            
            raw_name = coin_data.get("Coin name", "")
            if not raw_name: continue
            
            coin_key = raw_name.split()[0]
            
            if coin_key in wallets and coin_key in pools:
                coin_data['Wallet'] = wallets[coin_key]
                coin_data['Pool'] = pools[coin_key]
                coin_data['Key'] = coin_key 
                coins.append(coin_data)
                log(f" -> Kandydat: {coin_key} (${coin_data.get('Income per day in usd', 0):.2f})")
            else:
                pass

        except Exception as e:
            log(f"[WARN] Błąd parsowania danych: {e}")

    # 4. Wybór najlepszego
    if not coins:
        log("Brak pasujących coinów.")
        return None
        
    coins = sorted(coins, key=lambda x:x.get("Income per day in usd",0), reverse=True)
    best_one = coins[0]
    
    log(f"==> WYBRANO: {best_one['Key']} (Zysk: ${best_one.get('Income per day in usd', 0):.2f})")
    return best_one

def manage_worker(best_coin):
    if not best_coin:
        return

    coin_name = best_coin['Key']
    wallet = best_coin['Wallet']
    pool = best_coin['Pool']

    host_json_path = os.getenv('HOST_JSON_PATH')
    if not host_json_path:
        host_json_path = os.getcwd() + "/json"

    try:
        container = CLIENT.containers.get(CONTAINER_NAME)
        if container.status == 'running':
            if container.labels.get("mining_coin") == coin_name:
                log(f"[DOCKER] {coin_name} już pracuje. Stabilnie.")
                return
            else:
                log(f"[DOCKER] Zmiana! Zatrzymuję {container.labels.get('mining_coin')}...")
                container.stop()
                container.remove()
        else:
            container.remove()
    except docker.errors.NotFound:
        pass

    log(f"[DOCKER] Startuję XMrig: {coin_name} @ {pool}")
    
    cmd = f"--config=/config.json --coin \"{coin_name}\" -o {pool} -u {wallet} -p x -k --cpu-priority 0"
    
    try:
        CLIENT.containers.run(
            IMAGE_NAME,
            command=cmd,
            name=CONTAINER_NAME,
            detach=True,
            labels={"mining_coin": coin_name},
            privileged=True,
            network_mode="host",
            restart_policy={"Name": "unless-stopped"},
            volumes={
                f'{host_json_path}/config.json': {'bind': '/config.json', 'mode': 'ro'}
            }
        )
        log("[SUCCESS] Worker wystartował.")
    except Exception as e:
        log(f"[CRITICAL] Błąd startu workera: {e}")

if __name__ == "__main__":
    log("--- SmartMiner Manager v1.0 Started ---")
    
    while True:
        best = get_best_coin_logic()
        manage_worker(best)
        
        minutes = 15
        log(f"Uypianie na {minutes} minut...")
        time.sleep(minutes * 60)