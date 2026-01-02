import docker
import os
from docker.types import LogConfig
import config
from utils import log, save_dashboard_status

try:
    CLIENT = docker.from_env()
except Exception as e:
    log(f"[ERROR] Docker not found. Error: {e}", force=True)
    CLIENT = None

def stop_current_container():
    """Stops and removes the miner container."""
    if not CLIENT: return
    try:
        container = CLIENT.containers.get(config.CONTAINER_NAME)
        if container.status == 'running':
            log(f"[DOCKER] Stopping {config.CONTAINER_NAME}...", force=True)
            container.stop()
            container.remove()
            log("[DOCKER] Container removed.", force=True)
    except docker.errors.NotFound:
        pass
    except Exception as e:
        log(f"[ERROR] Error while stopping: {e}", force=True)

def manage_worker(best_coin, coins):
    """Manages worker lifecycle and switching decisions."""
    if config.state.miner_paused or not best_coin or not CLIENT:
        return

    new_coin_name = best_coin['Key']
    wallet = best_coin['Wallet']
    pool = best_coin['Pool']
    new_coin_income_usd = best_coin.get('Income per day in usd', 0)
    new_coin_income = best_coin.get("Income per day",0)
    new_coin_symbol = best_coin.get("Symbol",0)
    try:
        container = CLIENT.containers.get(config.CONTAINER_NAME)
        if container.status == 'running':
            old_coin_name = container.labels.get("mining_coin")
            
            if old_coin_name == new_coin_name:
                log(f"[DOCKER] {new_coin_name} is already running. Stable.")
                return

            old_coin_income_usd = 0
            for c in coins:
                if c.get("Key") == old_coin_name:
                    old_coin_income_usd = c.get('Income per day in usd', 0) * config.INCOME_TRESHOLD
                    break

            if old_coin_income_usd >= new_coin_income_usd:
                log(f"[INFO] Staying with {old_coin_name}. Profit increase too small (<{int((config.INCOME_TRESHOLD-1)*100)}%).")
                return

            log(f"[DOCKER] Switching! Stopping {old_coin_name}...")
            container.stop()
            container.remove()
        else:
            container.remove()
    except docker.errors.NotFound:
        pass

    log(f"[DOCKER] Starting XMrig: {new_coin_name} @ {pool}")
    
    cmd = f"--config=/config.json --coin \"{new_coin_name}\" -o {pool} -u {wallet} -p x -k --threads={config.MINER_THREADS}"
    
    try:
        CLIENT.containers.run(
            config.IMAGE_NAME,
            command=cmd,
            name=config.CONTAINER_NAME,
            detach=True,
            labels={"mining_coin": new_coin_name},
            privileged=True,
            network_mode="host",
            restart_policy={"Name": "unless-stopped"},
            volumes={
                f'{config.HOST_JSON_PATH}/config.json': {'bind': '/config.json', 'mode': 'ro'}
            },
            log_config=LogConfig(
            type='json-file',
            config={
                'max-size': '3m',
                'max-file': '3'
            }
        )
        )

        log(f"[SUCCESS] Worker {new_coin_name} has started.")
        save_dashboard_status(new_coin_name, pool, new_coin_income_usd,new_coin_income, new_coin_symbol)

    except Exception as e:
        log(f"[CRITICAL] Container startup error: {e}", force=True)