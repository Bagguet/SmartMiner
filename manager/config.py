import os
import threading

CONTAINER_NAME = "active_miner_worker"
IMAGE_NAME = "smartminer_worker_img:latest"
PATH_WALLETS = 'json/wallets.json'
PATH_POOLS = 'json/pools.json'
PATH_LINKS = 'links.txt'
PIPE_PATH = "/tmp/miner_comm"

MINER_THREADS = 1
MY_HASHRATE_KH = 17.3
INCOME_TRESHOLD = 1.05
HOURS_INTERVAL = 8

HOST_JSON_PATH = os.getenv('HOST_JSON_PATH', os.path.join(os.getcwd(), "json"))

class State:
    miner_paused = False
    logs_enabled = True
    wake_up_event = threading.Event()

state = State()

