"""
DISCORD BROADCASTER v1.0 — GHOST DAEMON
Sovereign Telemetry Sync via Synchronous httpx.
"""

import httpx
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BROADCASTER] %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

class DiscordBroadcaster:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def broadcast(self, message: str, title: str = "GHOST DAEMON STATUS", color: int = 3066993):
        """Broadcasts a clean, distraction-free coordinate ping to Discord."""
        payload = {
            "embeds": [{
                "title": f"🛡️ {title}",
                "description": message,
                "color": color,
                "footer": {"text": "Trishula Software | Sovereign Vigilance"}
            }]
        }

        try:
            with httpx.Client() as client:
                resp = client.post(self.webhook_url, json=payload, timeout=10.0)
                resp.raise_for_status()
                logger.info(f"Broadcast Success: {title}")
        except Exception as e:
            logger.error(f"Discord Broadcast Failed: {e}")

if __name__ == "__main__":
    # Test Block
    TEST_URL = "https://discordapp.com/api/webhooks/1478564245858811925/Z4NFf64hevTG7-PNPtRJVKeRVpaCCf12XhoIBUnB165HrrWh3Ft6vSGVRxpUA1_UM2fp"
    b = DiscordBroadcaster(TEST_URL)
    b.broadcast("Test manifest from local forge.", telemetry={"CPU": "5%", "RAM": "12% / 64GB"})
