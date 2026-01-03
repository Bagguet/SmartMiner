import threading
import config
from utils import log
from strategy import get_best_coin_logic
from miner_controller import manage_worker
from commands import listen_for_commands
import api_wrapper
from discord_service import start_discord_bot

if __name__ == "__main__":
    log("--- SmartMiner Manager v1.2 Started ---", force=True)
    try:
        start_discord_bot()
    except Exception as e:
        log(f"[WARN] Discord bot failed to start: {e}")

    listener_thread = threading.Thread(target=listen_for_commands, daemon=True)
    listener_thread.start()
    
    api_thread = threading.Thread(target=api_wrapper.run_server, daemon=True)
    api_thread.start()

    while True:
        config.state.wake_up_event.clear()
        
        if not config.state.miner_paused:
            best, coins = get_best_coin_logic()
            
            manage_worker(best, coins)
            
            log(f"[INFO] Next check in {config.HOURS_INTERVAL} hours...")
        else:
            log("[INFO] Miner is paused (use 'miner start' to resume).")

        config.state.wake_up_event.wait(timeout=config.HOURS_INTERVAL * 3600)