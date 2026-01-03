# ⛏️ SmartMiner Farm Dashboard

A real-time monitoring dashboard for cryptocurrency mining farms built with Streamlit. This dashboard provides unified monitoring of multiple mining workers, displaying hashrates, temperatures, uptime, and profitability metrics in a clean, responsive interface.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation--setup)
  - [Configuration](#1-configuration)
  - [Docker Setup](#2-running-with-docker-recommended)
  - [Local Development](#3-running-locally-development)
- [User Interface](#-user-interface-guide)
  - [KPI Overview](#kpi-overview)
  - [Worker Details](#worker-details)
- [Customization](#-customization)
  - [Refresh Rate](#refresh-rate)
  - [SSH Configuration](#ssh-links)
- [API Integration](#-api-integration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Real-time Monitoring
- **Total Farm Hashrate**: Combined hashrate across all workers with auto-scaling units (H/s to kH/s)
- **Worker Status**: Online/offline status with active worker count
- **Individual Worker Stats**: Detailed metrics for each mining rig

### Performance Metrics
- **Hashrate Tracking**: Real-time hashrate monitoring per worker
- **Share Statistics**: Accepted/rejected shares with accuracy rates
- **Uptime Monitoring**: Both miner process and system uptime
- **Temperature Sensors**: CPU and VRM temperature monitoring

### Financial Insights
- **Mining Target**: Current coin selection from manager
- **Profitability Estimates**: Daily profit calculations in USD and native coin

### Remote Management
- **SSH Integration**: One-click SSH access to worker nodes
- **Command Copy**: Quick copy-paste SSH commands
- **Network Status**: Real-time connectivity checking

### System Features
- **Configurable Refresh Rates**: 10-60 second intervals
- **Responsive Design**: Desktop and mobile compatible
- **Low Resource Footprint**: Optimized for continuous operation
- **Error Handling**: Graceful failure handling for offline workers

## 🏗️ Architecture

The dashboard consists of four main components:

- **`app.py`**: Main Streamlit application entry point
- **`data_provider.py`**: Handles API communication with mining nodes
- **`ui_components.py`**: Renders dashboard UI components and KPIs
- **`config.py`**: Configuration settings for miners and refresh rates

### Data Flow
1. Dashboard polls miners via HTTP API (port 4000)
2. Manager status read from JSON file
3. Data processed and displayed in real-time UI
4. Automatic refresh based on configured interval

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Bagguet/SmartMiner
   cd SmartMiner/dashboard
   ```

2. **Configure your miners**:
   ```bash
   cp config.example.py config.py
   # Edit config.py with your miner details
   ```

3. **Start with Docker** (recommended):
   ```bash
   docker compose up --build -d dashboard
   ```

4. **Access the dashboard** at [http://localhost:8501](http://localhost:8501)

## 📂 Installation & Setup

### 1. Configuration

Create your configuration file from the example:

```bash
cp config.example.py config.py
```

Edit `config.py` with your mining setup:

```python
# Mining workers configuration
MINERS_CONFIG = [
    {
        "name": "Rig1 - Ryzen 9 5950X",    # Display name
        "ip": "192.168.x.xx",              # Miner's local IP
        "port": 4000,                      # API port (must be 4000)
        "ssh_user": "miner0"               # SSH username
    },
    # Add more miners...
]

# Dashboard settings
REFRESH_RATE_SECONDS = 60    # Refresh interval (10-60 seconds)
API_TIMEOUT = 2              # API request timeout in seconds

# File paths
STATUS_JSON_PATH = '/app/json/status.json'      # Manager status file
CPU_TEMP_GLOB = '/sys/class/hwmon/hwmon*/temp*_input'  # CPU temp sensors
```

> **Important**: Use port 4000 (API Wrapper) for system statistics. Port 3000 (XMRig) doesn't provide comprehensive system metrics.

### 2. Docker Setup (Recommended)

The Docker setup provides a clean, isolated environment:

```bash
# Build and start the dashboard
docker compose up --build -d smartminer_dashboard

# View logs
docker compose logs -f smartminer_dashboard

# Stop the dashboard
docker compose down smartminer_dashboard
```

Access the dashboard at:
- http://localhost:8501
- http://YOUR_SERVER_IP:8501

### 3. Local Development (Development)

For development or testing without Docker:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Access the dashboard** at http://localhost:8501

## 🖥️ User Interface Guide

### KPI Overview

The top section displays key performance indicators for your entire mining farm:

- **Mining Target**: Current coin selection from the manager (e.g., "XMR")
- **Total Hashrate**: Combined hashrate of all online workers with auto-scaling units
  - Displays as H/s for low hashrates
  - Automatically scales to kH/s for higher values
- **Est. Farm Profit**: Projected daily earnings based on current hashrate
  - Primary display in USD
  - Secondary caption shows native coin amount
- **Worker Count**: Shows active workers vs total workers in the hashrate delta

### Worker Details

Each worker is displayed as a card with the following information:

#### Status Column
- **ON** (green): Worker is online and responding
- **OFF** (red): Worker is offline or not responding

#### Worker Information
- **Name**: Custom display name from configuration
- **IP Address**: Network address of the worker

#### Performance Metrics
- **Speed**: Current hashrate with auto-scaling units
- **Shares**: Accepted shares with accuracy percentage
  - Shows accepted share count
  - Delta displays acceptance rate percentage
  - Caption shows shares per minute

#### System Monitoring
- **Temperature**: CPU and VRM temperatures when available
  - CPU temperature always displayed if available
  - VRM temperature shown when detected
- **Uptime**: Dual uptime tracking
  - Miner: XMRig process uptime
  - System: Host machine uptime

#### Remote Access
- **Connect Button**: One-click SSH link (requires SSH protocol handler)
- **SSH Command**: Copy-paste ready SSH command for terminal use

## ⚙️ Customization

### Refresh Rate

Adjust the data refresh interval in the sidebar:

- **Range**: 10-60 seconds
- **Default**: 60 seconds (recommended for minimal CPU impact)
- **Lower values**: More frequent updates but higher resource usage
- **Higher values**: Less resource usage but slower data updates

## 🔌 API Integration

### Miner API Communication

The dashboard communicates with mining nodes through HTTP API calls:

- **Endpoint**: `http://{miner_ip}:4000/1/summary`
- **Method**: GET
- **Timeout**: Configurable (default 2 seconds)
- **Response Format**: JSON

#### Expected API Response Structure

```json
{
  "hashrate": {
    "total": [1234.5, "H/s"]
  },
  "uptime": 3600,
  "results": {
    "shares_good": 100,
    "shares_total": 105
  },
  "host": {
    "uptime": 86400
  },
  "sensors": {
    "cpu_temp": 65.5,
    "vrm_temp": 45.2
  }
}
```

### Manager Status

The dashboard reads mining manager status from a JSON file:

- **Path**: Configured via `STATUS_JSON_PATH` (default: `/app/json/status.json`)
- **Format**: JSON with coin and profitability information
- **Usage**: Displayed in KPI section for farm-wide metrics

#### Manager Status Format

```json
{
  "coin": "Monero",
  "profit_usd": 0.000001,
  "profit_coin": 0.0000001,
  "symbol": "XMR"
}
```
## 🤝 Contributing

We welcome contributions to improve the SmartMiner Dashboard!

### Development Setup

1. **Clone and setup**:
   ```bash
   git clone https://github.com/Bagguet/SmartMiner
   cd SmartMiner/dashboard
   cp config.example.py config.py
   pip install -r requirements.txt
   ```

2. **Run in development**:
   ```bash
   streamlit run app.py
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

<div align="center">
  <p>⚡ Powered by SmartMiner ⛏️</p>
  <p>Made with ❤️ for the crypto mining community</p>
</div>