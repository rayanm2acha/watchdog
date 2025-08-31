import requests
import subprocess
import time
from datetime import datetime
import sys
import json
import os

# === Load Config ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(
        "⚠️ config.json not found. Please copy config.example.json and fill it in."
    )

with open(CONFIG_PATH) as f:
    config = json.load(f)

URL = config["url"]
CONTAINER_NAME = config["container_name"]
CHECK_INTERVAL = config.get("check_interval", 60)
DISCORD_WEBHOOK_URL = config.get("discord_webhook_url")


def send_discord_alert(message):
    """Send a message to Discord via webhook."""
    if not DISCORD_WEBHOOK_URL:
        return
    try:
        payload = {"content": message}
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"{timestamp()} ⚠️ Failed to send Discord alert: {e}")


def check_service(url):
    """Check if the service is up by pinging the web UI."""
    try:
        return requests.get(url, timeout=5).status_code == 200
    except Exception:
        return False


def restart_container(container_name):
    """Restart the Docker container by name."""
    subprocess.run(["docker", "restart", container_name])
    msg = f"🔄 Restarted container: {container_name}"
    print(f"{timestamp()} {msg}")
    send_discord_alert(msg)


def timestamp():
    """Return a formatted timestamp string."""
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def watchdog(url, container_name, interval=60):
    """Main watchdog loop."""
    try:
        while True:
            if not check_service(url):
                msg = "⚠️ Service down. Restarting container..."
                print(f"{timestamp()} {msg}")
                send_discord_alert(msg)
                restart_container(container_name)
            else:
                print(f"{timestamp()} ✅ Check passed — Service is healthy")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{timestamp()} 👋 Watchdog stopped by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    watchdog(URL, CONTAINER_NAME, CHECK_INTERVAL)