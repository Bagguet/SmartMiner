# 🧠 SmartMiner Manager

The autonomous "brain" of the SmartMiner ecosystem, responsible for real-time market analysis, profit optimization, and containerized mining operations. This service continuously monitors mining profitability and automatically switches between coins to maximize returns. For a comprehensive overview and main setup instructions, please refer to the [main project README.md](../README.md).

## 📚 Table of Contents

- [🚀 Key Features](#-key-features)
  - [🔄 Autonomous Profit Switching](#-autonomous-profit-switching)
  - [🐳 Container Orchestration](#-container-orchestration)
  - [🌐 Advanced Web Scraping Engine](#-advanced-web-scraping-engine)
  - [Discord Notifications](#discord-notifications)
  - [🔌 Unified API (Port 4000)](#-unified-api-port-4000)
- [🛠️ Architecture](#-architecture)
  - [Core Components](#core-components)
  - [Data Flow Architecture](#data-flow-architecture)
- [📂 Configuration](#-configuration)
  - [1. Wallet Configuration (`json/wallets.json`)](#1-wallet-configuration-jsonwalletsjson)
  - [2. Mining Links (`links.txt`)](#2-mining-links-linkstxt)
  - [3. Discord Integration (`.env`)](#3-discord-integration-env)
  - [4. System Settings (`config.py`)](#4-system-settings-configpy)
  - [⚙️ Advanced Configuration Options](#-advanced-configuration-options)
- [📂 Output Files](#-output-files)
  - [`status.json`](#statusjson)
  - [`order.json`](#orderjson)
- [🔌 API Wrapper (Port 4000)](#-api-wrapper-port-4000)
  - [API Endpoint](#api-endpoint)
  - [Enhanced Response Format](#enhanced-response-format)
  - [Temperature Monitoring](#temperature-monitoring)
  - [System Integration](#system-integration)
- [🎮 Command Control](#-command-control)
  - [Available Commands](#available-commands)
  - [Command Processing](#command-processing)
- [🐳 Docker Deployment](#-docker-deployment)
  - [Prerequisites](#prerequisites)
  - [Container Privileges](#container-privileges)
  - [Quick Start](#quick-start)
  - [Required Volumes](#required-volumes)
- [🔧 Development & Debugging](#-development--debugging)
  - [Logging System](#logging-system)
  - [Debug Mode](#debug-mode)
  - [Common Debugging Commands](#common-debugging-commands)
  - [Error Handling](#error-handling)

---

## 🚀 Key Features

### 🔄 Autonomous Profit Switching
- **Real-time Analysis**: Monitors network hashrate, difficulty, and coin emission rates
- **Smart Switching**: Configurable profit threshold (default: +5%) prevents unnecessary switches
- **Scheduled Checks**: Automatic profitability analysis every 8 hours (configurable)
- **Multi-coin Support**: Analyzes Monero, Dagger, Etica, QuantumRL, Zephyr and more

### 🐳 Container Orchestration
- **Dynamic Docker Management**: Automatic XMRig container lifecycle management
- **Resource Optimization**: Configurable thread allocation and resource monitoring
- **Error Recovery**: Automatic restart and failure handling
- **Clean Switching**: Seamless transitions between mining coins

### 🌐 Advanced Web Scraping Engine
- **Headless Chromium**: Selenium-based JavaScript rendering for dynamic content
- **Anti-Bot Evasion**: Stealth techniques with user agent spoofing
- **Concurrent Processing**: Multi-threaded scraping for faster data collection
- **Fallback Mechanisms**: Error handling and retry logic for failed requests

### Discord Notifications
- **Real-time Alerts**: Instant notifications for miner events
- **Setup Notifications**: Automatic alerts for first-time configuration
- **Thread-Safe**: Async communication with error handling and retry logic

### 🔌 Unified API (Port 4000)
- **Enhanced Monitoring**: Combines XMRig statistics with host system metrics
- **Temperature Sensing**: Real-time CPU and VRM temperature monitoring
- **System Metrics**: Host uptime, performance data, and miner statistics
- **Dashboard Integration**: JSON responses optimized for dashboard consumption

## 🛠️ Architecture

### Core Components

| Component | Key Files | Responsibilities |
|-----------|-----------|------------------|
| **Main Loop** | `main.py` | • Orchestrates mining strategy<br>• Manages worker lifecycle<br>• Handles command interface<br>• Coordinates all services |
| **Strategy Engine** | `strategy.py` | • Profitability calculations<br>• Market data analysis<br>• Decision making logic<br>• Coin ranking and selection |
| **Container Manager** | `miner_controller.py` | • Docker container lifecycle<br>• Resource allocation<br>• Error handling and recovery<br>• Profit threshold validation |
| **Discord Service** | `discord_service.py` | • Bot authentication and messaging<br>• Real-time notifications<br>• Thread-safe communication<br>• Error handling |
| **Web Scraping** | `soupManager.py`, `jsTrigger.py` | • Dynamic content extraction<br>• Anti-bot evasion<br>• Data normalization<br>• Concurrent processing |
| **API Wrapper** | `api_wrapper.py` | • HTTP server on port 4000<br>• System sensor integration<br>• XMRig proxy functionality<br>• Dashboard data aggregation |
| **Command Interface** | `commands.py` | • Named pipe communication<br>• Real-time command processing<br>• State management<br>• Logging integration |
| **Utilities** | `utils.py` | • Logging system<br>• Dashboard status updates<br>• JSON file management<br>• Helper functions |

### Data Flow Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Sources   │───▶│   jsTrigger.py   │───▶│  soupManager.py │
│(MiningPoolStats)│    │ (Selenium)       │    │ (BeautifulSoup) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐             ▼
│ Discord Bot     │◀───│discord_service.py│    ┌─────────────────┐
│ (Notifications) │    │(Async Messaging) │    │  strategy.py    │
└─────────────────┘    └──────────────────┘    │ (Profit Engine) │
                                               └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐             ▼
│ Command Pipe    │◀───│   commands.py    │    ┌─────────────────┐
│(/tmp/miner_comm)│    │ (Named Pipe)     │    │   main.py       │
└─────────────────┘    └──────────────────┘    │ (Orchestrator)  │
                                               └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐             ▼
│ Dashboard (8501)│◀───│  api_wrapper.py  │    ┌─────────────────┐
│ (Monitoring)    │    │ (Port 4000)      │    │miner_controller │
└─────────────────┘    └──────────────────┘    │ (Docker Mgmt)   │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │ XMRig Container │
                                               │ (Mining Worker) │
                                               └─────────────────┘
```

## 📂 Configuration

The Manager requires specific configuration files to function properly. All files should be placed in the `json/` directory unless otherwise specified.

### 1. Wallet Configuration (`json/wallets.json`)

This file maps coin symbols to your wallet addresses. You should copy `json/wallets.example.json` to `json/wallets.json` and then edit it with your actual wallet addresses.

```json
{
  "Monero": "your_monero_wallet_address",
  "Dagger": "your_dagger_wallet_address",
  "Etica": "your_etica_wallet_address",
  "QuantumRL": "your_quantumrl_wallet_address",
  "Zephyr": "your_zephyr_wallet_address"
}
```

⚠️ **Security**: Add this file to `.gitignore`. Never commit your real wallet addresses.

### 2. Mining Links (`links.txt`)

This is a plain text file containing URLs to mining pool dashboards for scraping. You can create this file or copy it from `manager/links.example.txt` (if it exists) and then customize it.

```
https://miningpoolstats.stream/monero
https://miningpoolstats.stream/dagger
https://miningpoolstats.stream/etica_eti
https://miningpoolstats.stream/quantumrl
https://miningpoolstats.stream/zephyr
```

### 2. Discord Integration (`.env`)

Create a `.env` file with your Discord credentials:

```bash
DC_API_KEY=your_discord_bot_token_here
DC_USER_ID=your_discord_user_id_here
```

### 3. System Settings (`config.py`)

Core configuration parameters:

```python
# Mining Configuration
CONTAINER_NAME = "active_miner_worker"          # Docker container name
IMAGE_NAME = "smartminer_worker_img:latest"      # Docker image name
MINER_THREADS = 1                                # XMRig thread count

# Performance Settings
MY_HASHRATE_KH = 17.3                            # Your hashrate in kH/s
INCOME_TRESHOLD = 1.05                           # Profit increase threshold (5%)
HOURS_INTERVAL = 8                               # Check interval in hours

# File Paths
PATH_WALLETS = 'json/wallets.json'              # Wallet configuration
PATH_POOLS = 'json/pools.json'                   # Pool configuration  
PATH_LINKS = 'links.txt'                         # Mining links
PIPE_PATH = "/tmp/miner_comm"                    # Command pipe location
```

### ⚙️ Advanced Configuration Options

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| `HOURS_INTERVAL` | int | `8` | 1-24 | Profitability check interval (hours) |
| `INCOME_TRESHOLD` | float | `1.05` | 1.01-2.0 | Minimum profit increase to switch |
| `MY_HASHRATE_KH` | int | `17.3` | 1-10000 | Your hardware's hashrate in kH/s |
| `MINER_THREADS` | int | `1` | 1-64 | Number of CPU threads for XMRig |


## 📂 Output Files

The Manager service generates and updates the following JSON files in the shared `json/` directory to communicate with the Dashboard and external mining workers:

### `status.json`

This file contains real-time status updates for the Dashboard, including the currently mined coin, profitability metrics, and other relevant information.

```json
{
  "coin": "Monero",
  "profit_usd": 0.000001,
  "profit_coin": 0.0000001,
  "symbol": "XMR",
  "last_updated": "2024-01-01T12:30:00Z"
}
```

### `order.json`

This file dictates the current mining order for external slave miners. It specifies the coin to be mined. Slave miners are expected to read this file and adjust their operations accordingly.

```json
{
  "coin": "Monero",
  "pool": "pool.monero.org:3333",
  "wallet": "your_monero_wallet_address",
  "worker_id": "smartminer_worker_1",
  "last_updated": "2024-01-01T12:30:00Z"
}
```

## 🔌 API Wrapper (Port 4000)

The Manager hosts a specialized HTTP server on Port 4000 that enhances the raw XMRig API (Port 3000) with host system data. This is the primary interface for the Dashboard.

### API Endpoint

**GET** `/1/summary`

### Enhanced Response Format

```json
{
  // XMRig Statistics (from port 3000)
  "hashrate": {
    "total": [17300, "H/s"]
  },
  "uptime": 3600,
  "results": {
    "shares_good": 150,
    "shares_total": 152
  },
  
  // Enhanced System Data (added by wrapper)
  "sensors": {
    "cpu_temp": 65.5,
    "vrm_temp": 45.2
  },
  "host": {
    "uptime": 86400
  }
}
```

### Temperature Monitoring

- **CPU Temperature**: Reads from `/sys/class/hwmon/hwmon*/temp*_input`
- **VRM Temperature**: Monitors motherboard voltage regulator temperatures
- **Sensor Detection**: Automatically detects available temperature sensors
- **Error Handling**: Graceful fallback when sensors are unavailable

### System Integration

- **Uptime Tracking**: Host system uptime from `/proc/uptime`
- **Process Monitoring**: XMRig process statistics
- **Error Recovery**: Handles XMRig offline scenarios gracefully

## 🎮 Command Control

Control the manager in real-time using the named pipe interface:

### Available Commands

```bash
# Pause mining operations
echo "miner stop" > /tmp/miner_comm

# Resume mining operations  
echo "miner start" > /tmp/miner_comm
```
### Command Processing

- **Asynchronous Processing**: Commands are handled in real-time
- **State Management**: Commands update the global state immediately
- **Logging**: All commands are logged with timestamps
- **Error Handling**: Invalid commands are safely ignored

## 🐳 Docker Deployment

The Manager requires elevated privileges to control sibling containers and access hardware sensors.

### Prerequisites

- **Docker Engine**: 20.10.0 or later
- **Docker Compose**: 2.0.0 or later  
- **Socket Access**: Read/write access to `/var/run/docker.sock`
- **Hardware Access**: Read access to `/sys/class/hwmon` for temperature monitoring

### Container Privileges

The Manager container runs with elevated privileges:

```yaml
privileged: true
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
  - ./json:/app/json
  - /sys/class/hwmon:/sys/class/hwmon:ro
```

### Quick Start

```bash
# Build and start all services
docker-compose up -d --build

# View manager logs
docker-compose logs -f manager

# Check container status
docker-compose ps
```

### Required Volumes

| Volume | Purpose | Access |
|--------|---------|--------|
| `/var/run/docker.sock` | Container management | Read/Write |
| `./json` | Configuration and logs | Read/Write |
| `/sys/class/hwmon:ro` | Hardware sensors | Read-only |

## 🔧 Development & Debugging

### Logging System

The Manager uses a centralized logging system:

```python
# Standard logging
log("[INFO] Mining operation started")

# Forced logging (bypasses log disable)
log("[ERROR] Critical failure", force=True)
```

### Debug Mode

Enable detailed logging by setting `logs_enabled = True` in the state:

```python
config.state.logs_enabled = True
```

### Common Debugging Commands

```bash
# View real-time logs
docker-compose logs -f manager

# Check container status
docker exec smartminer_manager python -c "import config; print('Paused:', config.state.miner_paused)"

# Test API endpoint
curl http://localhost:4000/1/summary

# Send test command
echo "status" > /tmp/miner_comm
```

### Error Handling

- **Graceful Degradation**: Services continue operating when individual components fail
- **Retry Logic**: Automatic retries for network requests and container operations
- **Fallback Mechanisms**: Alternative data sources when primary sources fail
- **Comprehensive Logging**: All errors are logged with context and timestamps
---


<div align="center">
  <p>⚡ Powered by SmartMiner ⛏️</p>
  <p>Made with ❤️ for the crypto mining community</p>
</div>