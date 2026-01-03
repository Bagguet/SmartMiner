# ⛏️ SmartMiner - Autonomous Crypto Mining Farm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

SmartMiner is a fully automated, containerized cryptocurrency mining system designed for CPU mining (RandomX algorithms). It doesn't just mine; it thinks.

The system continuously scrapes real-time network data, calculates profitability based on your hardware, and automatically switches workers to the most profitable coin (Monero, Zephyr, Etica, QuantumRL, Dagger) using intelligent Docker orchestration.

## 🚀 Core Features

### 🧠 Intelligent Manager Service
- **Real-time Market Analysis**: Scrapes MiningPoolStats for network hashrate, difficulty, and coin emission data
- **Profit Optimization**: Automatically switches coins based on configurable profit thresholds (default 5% increase)
- **Smart Scheduling**: Analyzes profitability every 8 hours with configurable intervals
- **Container Orchestration**: Dynamic XMRig container lifecycle management with error recovery

### 📊 Live Dashboard Interface
- **Real-time Monitoring**: Streamlit-based web interface for farm-wide oversight
- **Multi-worker Support**: Monitor multiple mining rigs from a single dashboard
- **Hardware Metrics**: CPU/VRM temperatures, system uptime, and performance data
- **Financial Tracking**: USD and native coin profitability calculations
- **Remote Management**: One-click SSH access to worker nodes

### 🐳 Containerized Architecture
- **Docker-in-Docker**: Manager controls worker containers with elevated privileges
- **Optimized Workers**: XMRig containers with HugePages and MSR optimizations
- **Resource Management**: Configurable thread allocation and resource monitoring
- **Clean Switching**: Seamless transitions between mining coins without downtime

### 🌐 Advanced Web Scraping
- **Headless Chromium**: Selenium-based JavaScript rendering for dynamic content
- **Anti-Bot Evasion**: Stealth techniques with user agent spoofing
- **Concurrent Processing**: Multi-threaded scraping for faster data collection
- **Error Recovery**: Robust fallback mechanisms for failed requests

### 📱 Notifications & Control
- **Discord Integration**: Real-time alerts for miner events and coin switches
- **Command Interface**: Named pipe control for manual mining operations
- **API Wrapper**: Enhanced HTTP API (port 4000) with system sensor integration
- **Comprehensive Logging**: Detailed operation logs with error tracking

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SmartMiner Farm                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Manager       │  │   Dashboard     │  │   Workers       │  │
│  │   (Port 4000)   │  │   (Port 8501)   │  │   (Port 3000)   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Discord Bot     │  │ Web Scraper     │  │ Docker Engine   │  │
│  │ (Notifications) │  │ (Selenium)      │  │ (Orchestration) │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Command Pipe    │  │ API Wrapper     │  │ Hardware Sensors│  │
│  │ (/tmp/miner)    │  │ (Enhanced)      │  │ (CPU/VRM Temp)  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Mining Pool Networks                         │
│  (Monero, Zephyr, Etica, QuantumRL, Dagger)                     │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
SmartMiner/
├── manager/                 # 🧠 Autonomous "Brain"
│   ├── main.py             # Main orchestrator loop
│   ├── strategy.py         # Profitability analysis engine
│   ├── miner_controller.py # Docker container management
│   ├── api_wrapper.py      # Enhanced API server (port 4000)
│   ├── discord_service.py  # Discord bot integration
│   ├── jsTrigger.py        # Selenium web scraper
│   ├── soupManager.py      # BeautifulSoup data parser
│   ├── commands.py         # Named pipe command interface
│   ├── utils.py            # Logging and utilities
│   └── config.py           # Configuration settings
├── dashboard/               # 📊 Monitoring "Eyes"
│   ├── app.py              # Streamlit dashboard application
│   ├── ui_components.py    # Dashboard UI components
│   ├── data_provider.py    # API client for manager data
│   ├── config.py           # Dashboard configuration
│   └── requirements.txt    # Python dependencies
├── worker/                  # 💪 Mining "Muscle"
│   ├── Dockerfile          # Optimized XMRig image
├── json/                    # 📋 Configuration Files
│   ├── wallets.json        # Wallet addresses (secure)
│   ├── pools.json          # Mining pool configurations
│   ├── status.json         # Real-time status for dashboard
│   └── order.json          # Current mining orders
├── docker-compose.yml       # 🐳 Multi-service orchestration
└── README.md               # 📖 Project documentation
```

## 🚀 Quick Start

### Prerequisites

- **Operating System**: Linux (Ubuntu/Debian recommended) with kernel 4.0+
- **Docker**: Engine 20.10.0+ and Docker Compose 2.0.0+
- **Hardware**: CPU with AES-NI support, 4GB+ RAM (8GB+ recommended)
- **Network**: Internet access for mining pool data scraping
- **Optional**: HugePages enabled for maximum performance

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bagguet/SmartMiner.git
   cd SmartMiner
   ```

2. **Configure wallet addresses**
   ```bash
   cp json/wallets.example.json json/wallets.json
   # Edit with your actual wallet addresses
   ```

3. **Set up Discord notifications (optional)**
   ```bash
   cp manager/.example.env manager/.env
   # Edit with your Discord bot token and user ID
   ```
4. **Set up config for dashboard**
   ```bash
   cp dashboard/config.example.py dashboard/config.py
   # Edit with your worker configurations
   ```

5. **Start the complete stack**
   ```bash
   docker compose up -d --build
   ```

6. **Access the dashboard**
   ```
   http://localhost:8501
   # or http://YOUR_SERVER_IP:8501
   ```

### Initial Configuration

Edit the main configuration files:

**`json/wallets.json`** - Your wallet addresses:
```json
{
  "Monero": "your_monero_wallet_address",
  "Zephyr": "your_zephyr_wallet_address",
  "Etica": "your_etica_wallet_address"
}
```

**`json/pools.json`** - Mining pool configurations:
```json
{
  "Monero": "pool.monero.org:3333",
  "Zephyr": "zephyr.miningpoolstats.stream:5555",
  "Etica": "etica.miningpoolstats.stream:7777"
}
```

## 🎮 Management & Control

### Real-time Control

Control the mining manager using the command pipe:

```bash
# Pause mining operations
echo "miner stop" > /tmp/miner_comm

# Resume mining operations
echo "miner start" > /tmp/miner_comm

# Check current status
echo "status" > /tmp/miner_comm
```

### Monitoring & Logs

```bash
# View manager logs (brain activity)
docker compose logs -f manager

# View dashboard logs (UI activity)
docker compose logs -f dashboard

# View all services status
docker compose ps

# Check real-time API data
curl http://localhost:4000/1/summary
```

### Service Management

```bash
# Stop all mining operations
docker compose down

# Restart specific service
docker compose restart manager

# Update and rebuild
docker compose up -d --build
```

## 🔧 Advanced Configuration

### Manager Settings (`manager/config.py`)

```python
# Performance Tuning
MY_HASHRATE_KH = 17.3        # Your hardware hashrate in kH/s
INCOME_TRESHOLD = 1.05       # Profit increase threshold (5%)
HOURS_INTERVAL = 8           # Analysis interval in hours
MINER_THREADS = 1            # XMRig thread count

# Container Configuration
CONTAINER_NAME = "active_miner_worker"
IMAGE_NAME = "smartminer_worker_img:latest"
```

### Dashboard Settings (`dashboard/config.py`)

```python
# Worker Configuration
MINERS_CONFIG = [
    {
        "name": "Rig1 - Ryzen 9 5950X",
        "ip": "192.168.x.xx",
        "port": 4000,
        "ssh_user": "miner0"
    }
]

# Refresh Settings
REFRESH_RATE_SECONDS = 60    # Dashboard refresh interval
API_TIMEOUT = 2              # API request timeout
```

## 🔒 Security Considerations

### Container Security
- **Privileged Access**: Manager runs with elevated privileges for Docker control
- **Socket Access**: Requires access to `/var/run/docker.sock`
- **Hardware Access**: Read access to `/sys/class/hwmon` for temperature monitoring

### Data Protection
- **Wallet Security**: Wallet files are automatically excluded from git
- **Token Protection**: Discord tokens stored in `.env` files
- **Network Security**: Only run on trusted networks

### Recommended Practices
- Use dedicated mining system with limited user access
- Regularly update Docker and system packages
- Monitor logs for unusual activity
- Consider firewall rules for dashboard access

## 🤝 Contributing

We welcome contributions to improve SmartMiner!

### Development Setup

1. **Fork and clone** the repository
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** and test thoroughly
4. **Submit pull request** with detailed description

### Areas for Enhancement

- **Additional Coins**: Support for more RandomX-based cryptocurrencies
- **GPU Mining**: Extend support for GPU mining algorithms
- **Mobile App**: React Native or Flutter mobile interface
- **Database Integration**: Historical data storage and trend analysis
- **Alert System**: Email/webhook notifications for worker issues
- **Multi-User**: Authentication and role-based access control

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **XMRig** - High-performance CPU mining software
- **Streamlit** - Beautiful dashboard framework
- **MiningPoolStats** - Real-time mining pool statistics
- **Selenium** - Web automation and scraping
- **Docker** - Container orchestration platform

---

<div align="center">
  <p>⚡ Powered by SmartMiner ⛏️</p>
  <p>Made with ❤️ for the crypto mining community</p>
</div>