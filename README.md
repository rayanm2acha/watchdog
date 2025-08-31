# 🚀 Restart Watchdog

A lightweight Python watchdog that monitors a web service (such as [OctoBot](https://github.com/Drakkar-Software/OctoBot) running in Docker) and automatically restarts the container if the service becomes unavailable. Optional Discord integration lets you receive alerts when the service goes down or when a restart occurs.

## ✨ Features
- ✅ Periodic health checks via HTTP  
- 🔄 Automatic Docker container restarts on failure  
- 🔔 Optional Discord alerts (webhook)  
- 👋 Graceful shutdown on Ctrl+C  

## 📦 Installation
Clone this repository and install dependencies:
```bash
git clone https://github.com/YOUR_USERNAME/restart-watchdog.git
cd restart-watchdog
pip install -r requirements.txt