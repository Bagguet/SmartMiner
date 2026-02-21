import os
import threading

PATH_LINKS = 'links.txt'

MINER_THREADS = 31
MY_HASHRATE_KH = 17
INCOME_TRESHOLD = 1.05
HOURS_INTERVAL = 8



class State:
    miner_paused = False
    logs_enabled = True
    wake_up_event = threading.Event()

state = State()

