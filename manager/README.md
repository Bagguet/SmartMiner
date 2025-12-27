# 🧠 SmartMiner Manager

> The autonomous "brain" of the SmartMiner ecosystem, responsible for real-time market analysis, profit optimization, and containerized mining operations.

---

## 🚀 Key Features

### 🔄 Autonomous Profit Switching
- Real-time analysis of network hashrate, difficulty, and coin emission
- Smart switching with configurable profit threshold (default: +5%)
- Scheduled profitability checks (default: every 8 hours)

### 🐳 Container Orchestration
- Dynamic Docker container management for XMRig instances
- Automatic configuration based on optimal mining strategy
- Resource monitoring and optimization

### 🌐 Web Scraping Engine
- Headless Chromium with Selenium for dynamic content
- Custom parsers for major mining pools
- Fallback mechanisms for failed scrapes

### 🔌 Unified API (Port 4000)
- Combines XMRig statistics with host system metrics
- Real-time monitoring of CPU temperature, uptime, and performance
- Dashboard-compatible JSON responses

## 🛠️ Architecture

### Core Components

| Component | Key Files | Responsibilities |
|-----------|-----------|------------------|
| **Main Loop** | `main.py` | • Orchestrates mining strategy<br>• Manages worker lifecycle<br>• Handles command interface |
| **Strategy Engine** | `strategy.py` | • Profitability calculations<br>• Market data analysis<br>• Decision making logic |
| **Container Manager** | `miner_controller.py` | • Docker container lifecycle<br>• Resource allocation<br>• Error handling and recovery |
| **Web Scraping** | `soupManager.py`, `jsTrigger.py` | • Dynamic content extraction<br>• Anti-bot evasion<br>• Data normalization |

## 📂 Configuration

The Manager requires specific JSON files to function. Ensure these exist in the json/ directory.

1. Wallets (json/wallets.json)

Map coin names (keys) to your wallet addresses. ⚠️ Security: Add this file to .gitignore. Do not commit your real addresses.

2. Pools (json/pools.json)

Map coin names to your preferred mining pools (host:port).

3. Links (links.txt)

A plain text file containing URLs to mining pool dashboards or explorer pages that the scraper should analyze.

4. System Settings

### ⚡ Configuration Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `HOURS_INTERVAL` | int | `8` | Profitability check interval (hours) |
| `INCOME_THRESHOLD` | float | `1.05` | Minimum profit increase to switch (5%) |
| `MY_HASHRATE_KH` | int | `1000` | Your hardware's hashrate in kH/s |


## 🔌 API Wrapper (Port 4000)

The Manager hosts a specialized HTTP server on Port 4000. Unlike the raw XMRig API (Port 3000), this wrapper injects Host System Data.

Endpoint: GET /1/summary Response:

The Dashboard relies on this port to show temperatures.

## 🎮 Command Control

Control the manager via named pipe:

```bash
# Pause mining
echo "miner stop" > /tmp/miner_comm

# Resume mining
echo "miner start" > /tmp/miner_comm

# Check status
echo "status" > /tmp/miner_comm
```

> 🔄 Commands are processed asynchronously. Check logs for confirmation.

## 🐳 Docker Deployment

The Manager requires specific privileges to control sibling containers and access hardware sensors.

### Prerequisites
- Docker Engine 20.10.0 or later
- Docker Compose 2.0.0 or later
- Access to `/var/run/docker.sock`
- Read access to `/sys/class/hwmon` for temperature monitoring

### Quick Start
```bash
docker-compose up -d
```
### Required Volumes
- `/var/run/docker.sock` - For container management
- `./json` - Configuration and logs directory
- `/sys/class/hwmon:ro` - Read-only access to hardware sensors

## 🔧 Troubleshooting

- Temperature shows "0" or "N/A": Ensure /sys is mounted read-only (ro) in the Docker volume configuration. The API wrapper looks for sensors in /sys/class/hwmon/.

- Worker not starting: Check the Manager logs (docker logs smartminer_manager). Ensure the coin name scraped from the web matches a key in wallets.json and pools.json.

---

<div align="center">
  <p>⚡ Powered by SmartMiner ⛏️</p>
</div>