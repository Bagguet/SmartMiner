# ⛏️ SmartMiner Farm Dashboard

A lightweight, real-time monitoring interface for the SmartMiner ecosystem. Built with Streamlit, this dashboard provides a unified view of your mining farm's health, hashrate, and profitability.

## 📋 Table of Contents

- [Dashboard Preview](#-dashboard-preview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation](#-installation--setup)
  - [Configuration](#1-configuration)
  - [Docker Setup](#2-running-with-docker-recommended)
  - [Local Development](#3-running-locally-development)
- [User Interface](#-user-interface-guide)
  - [Dashboard Overview](#dashboard-overview)
  - [Worker Details](#worker-details)
- [Customization](#-customization)
  - [Refresh Rate](#refresh-rate)
  - [SSH Configuration](#ssh-links)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 📊 Dashboard Preview

![SmartMiner Dashboard Screenshot](images/screenshot.png)

*Figure: SmartMiner Dashboard showing real-time mining statistics and worker status*

## ✨ Features

- **Real-time Monitoring**
  - Total farm hashrate and individual worker speeds
  - Active worker count and status
  - Detailed worker statistics

- **Financial Insights**
  - Current mining target (Coin)
  - Estimated daily profit in USD

- **System Health**
  - CPU temperature monitoring
  - Application and system uptime
  - Resource utilization metrics

- **Remote Management**
  - One-click SSH access
  - Copy-paste SSH commands
  - Quick terminal access

- **Performance**
  - Configurable refresh rates
  - Responsive design (desktop & mobile)
  - Low resource footprint

## 🛠️ Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)
- Network access to miners (port 4000)
- SSH access to worker nodes

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/Bagguet/SmartMiner
   cd smartminer-dashboard/dashboard
   ```

2. Copy and configure the example config:
   ```bash
   cp config.example.py config.py
   # Edit config.py with your miner details
   ```

3. Start with Docker:
   ```bash
   docker compose up --build -d dashboard
   ```

4. Access the dashboard at [http://localhost:8501](http://localhost:8501)

## 📂 Installation & Setup

### 1. Configuration

1. Navigate to the dashboard directory:
   ```bash
   cd dashboard/
   ```

2. Copy and edit the configuration file:
   ```bash
   cp config.example.py config.py
   nano config.py  # or use your preferred editor
   ```

3. Configure your miners in `config.py`:
   ```python
   MINERS_CONFIG = [
       {
           "name": "Rig1",          # Display name
           "ip": "192.168.x.xx",    # Miner's local IP
           "port": 4000,            # Must be 4000 for system stats
           "ssh_user": "miner0"     # SSH username
       },
       # Add more miners...
   ]
   
   # Refresh interval in seconds (10-60)
   REFRESH_RATE_SECONDS = 60
   ```

   > **Note**: Use port 4000 (API Wrapper) for system stats. Port 3000 (XMRig) doesn't provide system statistics.

### 2. Running with Docker (Recommended)

```bash
docker compose up --build -d dashboard
```

Access the dashboard at:
- http://localhost:8501
- http://192.168.x.xx:8501

### 3. Running Locally (Development)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 🖥️ User Interface Guide

### Dashboard Overview

The dashboard provides an at-a-glance view of your mining operation:

- **Mining Target**: Currently selected coin
- **Total Hashrate**: Combined hashrate of all workers
- **Est. Farm Profit**: Projected daily earnings
- **Active Workers**: Number of online miners

### Worker Details

Each worker card displays:

- **Status**: <span style="color: #4CAF50;">ONLINE</span> / <span style="color: #F44336;">OFFLINE</span>
- **Speed**: Current hashrate (auto-scales from H/s to MH/s)
- **Shares**: Accepted/rejected shares with accuracy
- **Temperature**: CPU temperature with color indicators
- **Uptime**: 
  - Miner: XMRig process uptime
  - System: Host machine uptime
- **SSH Access**: One-click connection or copy command

## ⚙️ Customization

### Refresh Rate

Adjust the polling interval in the sidebar:
- Range: 10-60 seconds
- Default: 60 seconds (recommended for minimal CPU impact)

### SSH Links

The dashboard provides SSH access in two ways:

1. **Connect Button**: One-click access (requires `ssh://` protocol handler)
2. **Copy Command**: Manual SSH command for terminal use

**Platform Notes**:
- **Windows**: Requires PuTTY or Windows Terminal with SSH support
- **Linux/macOS**: May need to register `x-scheme-handler/ssh`


---

<div align="center">
  <p>⚡ Powered by SmartMiner ⛏️</p>
</div>