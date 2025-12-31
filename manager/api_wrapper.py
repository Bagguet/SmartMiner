import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import psutil

# Configuration
XMRIG_HOST = "127.0.0.1"
XMRIG_PORT = 3000
MY_PORT = 4000  # Port for serving the "enhanced" JSON

def get_temps():
    temps = psutil.sensors_temperatures()
    VRM_temp = 0
    CPU_temp = 0
    # CPU temperature
    if 'k10temp' in temps:
        Tccd1 = 0
        Tccd2 = 0
        for entry in temps['k10temp']:
            if entry.label == "Tccd1":
                Tccd1 = float(entry.current)
            elif entry.label == "Tccd2":
                Tccd2 = float(entry.current)
        try: 
            CPU_temp = max(Tccd1,Tccd2)
        except:
            CPU_temp = 0

    # VRM temperature
    if 'nct6687' in temps:
        for entry in temps['nct6687']:
            if entry.label == "Thermistor 15":
                VRM_temp = entry.current
    return CPU_temp, VRM_temp


def get_system_uptime():
    """Reads the host (system) uptime in seconds."""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return int(uptime_seconds)
    except:
        return 0

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(404)
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        final_data = {}
        try:
            url = f"http://{XMRIG_HOST}:{XMRIG_PORT}{self.path}"
            resp = requests.get(url, timeout=2)
            final_data = resp.json()
        except:
            final_data = {"error": "XMRig offline"}

        CPU_temp, VRM_temp = get_temps()

        final_data['sensors'] = {
            'cpu_temp': CPU_temp,
            'vrm_temp': VRM_temp,
        }

        final_data['host'] = {
            'uptime': get_system_uptime()
        }

        self.wfile.write(json.dumps(final_data).encode('utf-8'))

    def log_message(self, format, *args):
        return

def run_server():
    server_address = ('0.0.0.0', MY_PORT)
    httpd = HTTPServer(server_address, ProxyHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()