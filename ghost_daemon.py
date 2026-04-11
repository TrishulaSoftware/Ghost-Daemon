"""
GHOST DAEMON v1.0 — CORE WATCHDOG
Resilient Process Guard & Telemetry Nexus.
"""

import os
import sys
import time
import yaml
import psutil
import requests
import logging
import subprocess
from pathlib import Path
from services.discord_broadcaster import DiscordBroadcaster

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [DAEMON] %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

class GhostDaemon:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.broadcaster = DiscordBroadcaster(self.config['discord_webhook'])
        self.retry_count = 0
        self.max_retries = 5
        self.backoff_sequence = [2, 4, 8, 16, 32]
        self.ngrok_path = Path(self.config['ngrok_path'])
        self.ngrok_port = self.config['ngrok_port']

    def _load_config(self, path: str):
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.critical(f"Config Ingestion Failure: {e}")
            sys.exit(1)

    def find_ngrok_pid(self):
        """Locate active ngrok process."""
        for proc in psutil.process_iter(['pid', 'name']):
            if 'ngrok' in proc.info['name'].lower():
                return proc.info['pid']
        return None

    def query_ngrok_url(self):
        """Verify tunnel state via local API."""
        try:
            resp = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            resp.raise_for_status()
            tunnels = resp.json().get('tunnels', [])
            for t in tunnels:
                if t.get('proto') == 'https':
                    return t.get('public_url')
        except:
            return None
        return None

    def remediate(self):
        """Deterministic remediation with exponential backoff."""
        if self.retry_count >= self.max_retries:
            self.broadcaster.broadcast(
                "CRITICAL: Ghost Daemon failed 5 remediation attempts. LOUD KILL EXECUTED.",
                title="TERMINAL FAILURE",
                color=15158332 # Red
            )
            logger.critical("EXCEEDED MAX RETRIES. SELF-TERMINATING.")
            sys.exit(1)

        wait_time = self.backoff_sequence[self.retry_count]
        logger.warning(f"Remediation Start (Attempt {self.retry_count + 1}). Backoff: {wait_time}s")
        
        # Kill any zombie ngrok
        for proc in psutil.process_iter(['name']):
            if 'ngrok' in proc.info['name'].lower():
                proc.kill()
        
        time.sleep(1)
        
        # Kick ngrok
        try:
            subprocess.Popen([str(self.ngrok_path), "http", str(self.ngrok_port)], 
                             creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            time.sleep(wait_time)
            
            url = self.query_ngrok_url()
            if url:
                logger.info(f"Remediation Success: {url}")
                self.broadcaster.broadcast(
                    f"Tunnel Restored: **{url}**",
                    title="REMEDIATION SUCCESS"
                )
                self.retry_count = 0 # Reset
                return True
            else:
                self.retry_count += 1
                return False
        except Exception as e:
            logger.error(f"Execution Fault: {e}")
            self.retry_count += 1
            return False

    def run(self):
        logger.info("Ghost Daemon Active. Monitoring Sovereignty.")
        while True:
            pid = self.find_ngrok_pid()
            if not pid:
                logger.warning("Sovereignty Breach: Ngrok PID not found.")
                self.remediate()
            else:
                # Periodic URL check
                url = self.query_ngrok_url()
                if not url:
                    logger.warning("Tunnel Ghosting Deteced. remediating.")
                    self.remediate()
            
            time.sleep(60) # High-efficiency watch

if __name__ == "__main__":
    daemon = GhostDaemon("config.yaml")
    daemon.run()
