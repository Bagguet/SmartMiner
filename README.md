# SmartMiner - Autonomous Crypto Mining Docker Cluster ⛏️🤖

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![XMrig](https://img.shields.io/badge/Miner-XMrig-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**SmartMiner** to w pełni autonomiczny, skonteneryzowany system do wydobywania kryptowalut (CPU Mining), który dynamicznie przełącza się na najbardziej opłacalny algorytm w czasie rzeczywistym.

System wykorzystuje **Selenium (Stealth)** do analizy rynku, **Docker API** do orkiestracji kontenerów oraz **XMrig** z dostępem niskopoziomowym do sprzętu.

> ⚠️ **HW OPTIMIZATION NOTICE:** > Domyślna konfiguracja (`config.json`) oraz parametry startowe kontenera są zoptymalizowane pod procesor **AMD Ryzen 9 5950X** (16C/32T, 64MB L3 Cache).
> * Włączone Huge Pages (1GB).
> * MSR Registers Mod włączony.
> * Specyficzne mapowanie wątków RandomX.
> * *Uruchamiając na innym CPU, zaleca się dostosowanie `json/config.json`.*

---

## 🚀 Główne Funkcje

* **📈 Analiza Rynku Live:** Bot (Python + Selenium) cyklicznie skanuje MiningPoolStats, pobierając hashrate sieci, emisję, cenę i trudność.
* **🧠 Inteligentny Wybór:** Automatycznie oblicza opłacalność (USD/dzień) dla zdefiniowanych coinów (Monero, Zephyr, Dagger, etc.) i wybiera zwycięzcę.
* **🐳 Docker Orchestration:** Manager automatycznie zabija stary kontener koparki i stawia nowy z odpowiednim algorytmem, bez przerywania działania systemu hosta.
* **ghost-mode:** Zaawansowana konfiguracja Selenium (`undetected-chromedriver` / `selenium-stealth`) omija zabezpieczenia Cloudflare.
* **⚡ Hardware Tuning:** Kontenery działają w trybie uprzywilejowanym (`privileged`), co pozwala na pełną akcelerację sprzętową (MSR, HugePages) wewnątrz wirtualizacji.

---

## 🛠️ Struktura Projektu

```text
SmartMiner/
├── docker-compose.yml       # Orkiestrator całego klastra
├── manager/                 # Mózg operacji (Python)
│   ├── main.py              # Główna pętla decyzyjna i sterowanie Dockerem
│   ├── jsTrigger.py         # Moduł Stealth Web Scraping (Selenium)
│   ├── soupManger.py        # Parser danych HTML (BeautifulSoup)
│   └── Dockerfile           # Środowisko managera
├── worker/                  # Ramię robocze (XMrig)
│   └── Dockerfile           # Kompilacja XMriga ze źródeł
└── json/                    # Konfiguracja dynamiczna (montowana jako Volume)
    ├── config.json          # Bazowa konfiguracja XMriga (Ryzen 5950X tuned)
    ├── wallets.json         # Twoje adresy portfeli
    └── pools.json           # Adresy pooli wydobywczych
```
---

## Instalacja i Uruchomienie

### Wymagania
* Linux (zalecane Ubuntu/Debian)
* Docker & Docker Compose V2
* Procesor z obsługą instrukcji AES

### 1. Klonowanie repozytorium
git clone https://github.com/Bagguet/SmartMiner.git
cd SmartMiner

### 2. Konfiguracja Portfeli
Projekt zawiera przykładowy plik portfeli. Musisz go uzupełnić swoimi danymi.

cp json/wallets.example.json json/wallets.json
nano json/wallets.json

*Upewnij się, że klucze w pliku wallets.json odpowiadają nazwom coinów na MiningPoolStats (np. "Monero", "Zephyr").*

### 3. Uruchomienie (Auto-Build)
Najprostszy sposób. Docker Compose automatycznie zbuduje obrazy.

docker compose up --build -d

### 4. Podgląd Logów

# Logi Managera (Decyzje finansowe)
docker compose logs -f manager

# Logi Workera (Hashrate i Shares)
docker logs -f active_miner_worker

---

## Bezpieczne Zatrzymywanie
Ponieważ Worker jest uruchamiany dynamicznie przez skrypt Pythona (poza docker-compose), standardowe "down" może nie wystarczyć.

1. Zatrzymaj Managera:
docker compose down

2. Zabij proces koparki (jeśli nadal działa w tle):
docker rm -f active_miner_worker

---
