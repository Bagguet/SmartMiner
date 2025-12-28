import json
import glob
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Configuration
XMRIG_HOST = "127.0.0.1"
XMRIG_PORT = 3000
MY_PORT = 4000  # Port for serving the "enhanced" JSON

def get_cpu_temp():
    """Reads temperature from the system (same as in the dashboard)."""
    try:
        files = glob.glob('/sys/class/hwmon/hwmon*/temp*_input')
        temps = []
        for file in files:
            try:
                with open(file, 'r') as f:
                    val = int(f.read().strip())
                    if val > 0: temps.append(val)
            except: pass
        
        if temps:
            max_temp = max(temps)
            return max_temp / 1000.0 if max_temp > 1000 else max_temp
    except Exception as e:
        print(f"Temperature read error: {e}")
    return 0

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

        temp = get_cpu_temp()

        final_data['sensors'] = {
            'cpu_temp': temp,
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