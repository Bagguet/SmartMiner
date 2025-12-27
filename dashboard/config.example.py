LOG_FILE_TEMP = "temperature_log.txt"
LOG_FILE_HASH = "hashrate_log.txt"

STATUS_JSON_PATH = '/app/json/status.json'
CPU_TEMP_GLOB = '/sys/class/hwmon/hwmon*/temp*_input'

MINERS_CONFIG = [
    {
        "name": "Rig1 - ryzen 9 5950x",
        "ip": "192.168.x.xx",
        "port": 4000,
        "ssh_user": "miner0"
    },
    {
        "name": "Laptop",
        "ip": "192.168.x.xx", 
        "port": 4000,
        "ssh_user": "bgieta"
    },
]

REFRESH_RATE_SECONDS = 60
API_TIMEOUT = 2