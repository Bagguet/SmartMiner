# ⛏️ SmartMiner - Autonomous Crypto Mining Farm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

SmartMiner is a fully automated, containerized cryptocurrency mining system designed for CPU mining (RandomX). It doesn't just mine; it thinks.

The system scrapes real-time network data, calculates profitability based on your hardware, and automatically switches your workers to the most profitable coin (e.g., Monero, Zephyr, Etica) using Docker-in-Docker orchestration.

## ✨ Features

- 🧠 **Intelligent Manager**: Continuously analyzes network hashrate, difficulty, and coin emission to maximize USD daily profit
- 📊 **Live Dashboard**: Beautiful Streamlit interface to monitor hashrate, system temps, and financial metrics in real-time
- 🐳 **Dockerized Workers**: Ephemeral XMRig containers that are created and destroyed dynamically
- 🌡️ **Hardware Monitoring**: Reads CPU temperatures and system uptime via a custom API wrapper
- ⚡ **Optimized**: Supports HugePages and MSR registers for maximum hash output
- 🔄 **Auto-Switching**: Automatically switches to the most profitable coin based on real-time data

## 🏗️ Project Structure

```
SmartMiner/
├── manager/          # The "Brain" - Scrapes data, decides strategy, controls Docker
├── worker/           # The "Muscle" - Optimized XMRig image build context
├── dashboard/        # The "Eyes" - Web UI for monitoring and control
├── json/             # Configuration files
│   ├── config.json   # Main configuration
│   ├── wallets.json  # Wallet addresses
│   └── pools.json    # Mining pool configurations
└── docker-compose.yml # Docker Compose configuration
```

## Quick Start

### Prerequisites

- **OS**: Linux (Ubuntu/Debian recommended) with kernel 4.0+
- **Docker**: Engine 20.10.0+ and Docker Compose plugin
- **Hardware**: CPU with AES-NI support, 4GB+ RAM (8GB+ recommended)
- **Recommended**: HugePages enabled on the host system

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SmartMiner.git
   cd SmartMiner
   ```

2. **Configure your settings**
   ```bash
   cp json/wallets.example.json json/wallets.json
   cp manager/links.example.txt manager/links.txt
   # Edit these files with your wallet addresses and preferred pools
   ```

3. **Start the stack**
   ```bash
   docker compose up -d
   ```

4. **Access the dashboard**
   ```
   http://192.168.x.xx:8501
   ```

## 🛠️ Management

### Viewing Logs

```bash
# View manager logs
docker compose logs -f manager

# View dashboard logs
docker compose logs -f dashboard
```

### Stopping the Miner

```bash
docker compose down
```

## 🔒 Security Notes

- The Manager runs in privileged mode with access to the Docker socket. Only run this on trusted networks.
- Wallet configuration files are automatically added to `.gitignore` but always double-check before committing.
- Consider using a dedicated system user with limited permissions for running the containers.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- XMRig for the mining software
- Streamlit for the dashboard framework
- MiningPoolStats for pool data