import os
import time
import config
from utils import log
from miner_controller import stop_current_container

def listen_for_commands():
    """Background thread that listens for text commands."""
    
    # Create a PIPE if it doesn't exist
    if not os.path.exists(config.PIPE_PATH):
        try:
            os.mkfifo(config.PIPE_PATH)
        except OSError as e:
            log(f"[ERROR] Failed to create pipe: {e}", force=True)
            return

    log(f"[SYSTEM] Listening for commands in {config.PIPE_PATH}...", force=True)
    
    while True:
        try:
            # Otwarcie potoku w trybie odczytu
            with open(config.PIPE_PATH, "r") as pipe:
                for line in pipe:
                    cmd = line.strip().lower()
                    
                    if cmd == "miner stop":
                        config.state.miner_paused = True
                        log("!!! RECEIVED COMMAND: MINER STOP !!!", force=True)
                        stop_current_container()
                        
                    elif cmd == "miner start":
                        config.state.miner_paused = False
                        log("!!! RECEIVED COMMAND: MINER START !!!", force=True)
                        # Wake up the main manager loop
                        config.state.wake_up_event.set()
                        
                    elif cmd == "status":
                        status = "PAUSED" if config.state.miner_paused else "RUNNING"
                        log(f"[STATUS] Mode: {status} | Logs: {config.state.logs_enabled}", force=True)
                    
                    elif cmd == "exit":
                        log("[SYSTEM] Received termination command...", force=True)
                        # Here you can add safe shutdown logic for the entire manager
        except Exception as e:
            log(f"[PIPE ERROR] {e}", force=True)
            time.sleep(1)