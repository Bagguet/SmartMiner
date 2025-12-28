import json
import requests
import glob
import config

def get_manager_status():
    try:
        with open(config.STATUS_JSON_PATH, 'r') as f: 
            return json.load(f)
    except: 
        return None

def get_all_miners_stats():
    """Retrieves statistics from all defined miners."""
    results = []
    
    for miner in config.MINERS_CONFIG:
        url = f"http://{miner['ip']}:{miner['port']}/1/summary"
        status_data = {
            "name": miner.get('name'),
            "ip": miner.get('ip'),
            "ssh_user": miner.get('ssh_user'),
            "online": False,
            "hashrate": 0,
            "uptime": 0,
            "shares_good": 0,
            "shares_bad": 0,
            "raw_data": None
        }

        try:
            response = requests.get(url, timeout=config.API_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                status_data["online"] = True
                status_data["raw_data"] = data
                # hashrate
                if 'hashrate' in data:
                    status_data["hashrate"] = data['hashrate']['total'][0]
                # miner uptime
                if 'uptime' in data:
                    status_data["uptime"] = data['uptime']
                # system uptime
                if 'host' in data and 'uptime' in data['host']:
                    status_data["sys_uptime"] = data['host']['uptime']
                # shares
                if 'results' in data:
                    status_data["shares_good"] = data['results'].get('shares_good', 0)
                    try:
                        status_data["shares_bad"] = int(data['results'].get('shares_total', 0)) - int(status_data["shares_good"])
                    except:
                        status_data["shares_bad"] = 0
                # CPU temperature
                if 'sensors' in data and 'cpu_temp' in data['sensors']:
                    status_data["remote_temp"] = data['sensors']['cpu_temp']
                
        except:
            pass 
            
        results.append(status_data)
        
    return results