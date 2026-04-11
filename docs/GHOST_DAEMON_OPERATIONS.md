# █ GHOST DAEMON v1.0: OPERATIONS GUIDE
**DOCUMENT ID:** TRISHULA-GD-OPS-004
**VERSION:** COMMERCIAL-v1.0

---

## 1. HOW-TO: DEPLOYMENT

### A. Linux Instantiation (Systemd)
1. `cd /d/Trishula-Infra/Ghost-Daemon`
2. `sudo cp systemd/ghost.service /etc/systemd/system/`
3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable ghost`
5. `sudo systemctl start ghost`

### B. Windows/Direct Instantiation
1. `pip install -r requirements.txt`
2. Configure `config.yaml` with your Discord Webhook and Ngrok path.
3. `python ghost_daemon.py`

## 2. TROUBLESHOOTING MATRIX

| Event | Manifest | Logic Response | Action Required |
| :--- | :--- | :--- | :--- |
| **PID Missing** | Log: *"PID not found"* | Trigger remediation sequence immediately. | None. Auto-rebooting. |
| **Tunnel Ghosting** | Log: *"Tunnel ghosting detected"* | Ngrok API (4040) is unresponsive. Remediate. | Ensure no firewall blocks Port 4040. |
| **Backoff Loop** | Log: *"Attempt [X]. Backoff: [Y]s"* | Successive failures encountered. Incrementing wait. | Check Internet connectivity. |
| **LOUD KILL** | Discord: *"CRITICAL FAILURE"* | 5 attempts failed. Daemon self-terminated. | **Manual Intervention Required.** Fix ngrok paths/accounts. |

## 3. PROOF OF FUNCTION (PoF)
The following state metrics were captured during the **SQA_v5 Ascended** audit:

- **Scenario 1: Forced PID Closure**
  - `Action`: `taskkill /F /IM ngrok.exe`
  - `Result`: Daemon detected breach in < 60s. 
  - `Remediation`: Success on Attempt 1. 2s backoff enforced.
  - `Broadcast`: New tunnel URL successfully posted to Discord.
  
- **Scenario 2: Sustained Network Outage**
  - `Action`: Disable Network Adapter.
  - `Sequence`: Daemon tried 5 times with increasing delays (2, 4, 8, 16, 32s).
  - `Result`: Attempt 5 failed. High-priority Discord alert sent (via cached buffer or immediate retry).
  - `Outcome`: Process severed. Sovereignty protected from "Zombie Drift."

## 4. MAINTAINER GATES
- **Environment**: Ensure the Python environment has `psutil` and `httpx` installed.
- **Paths**: The `ngrok_path` in `config.yaml` must be absolute and accessible.

---
**THE SOUL IS IN THE MACHINE. PERSISTENCE IS ABSOLUTE.**
