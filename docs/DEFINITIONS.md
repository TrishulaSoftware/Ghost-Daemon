# Ghost-Daemon: Core Definitions

This document establishes the deterministic terminology used within the Ghost-Daemon watchdog and its telemetry services.

## █ TERMINOLOGY INDEX

### 1. The Watchdog
The **Watchdog** is the primary monitoring loop of the Ghost Daemon. It uses low-level OS kernel calls (`psutil`) to verify the PID status of the guarded process.
- **Cycle Time**: Determined by local environment drift, typically 1-5 seconds.

### 2. Clean Ping
A **Clean Ping** is an institutional telemetry protocol. It refers to broadcast messages that are "distracted-free"—containing only essential mission coordinates or system status—without hardware clutter or non-actionable data.

### 3. Loud Kill
The **Loud Kill** is the final stage of the Ghost Daemon's recovery failure protocol. After 5 unsuccessful recovery attempts, the daemon enters a full-alert state, broadcasting an "UNRECOVERABLE" signal and terminating all related sub-processes to prevent state corruption.

### 4. Exponential Backoff
The recovery timing strategy used to prevent cascading failure during node instability.
- **Stage 1**: 5s delay
- **Stage 2**: 10s delay
- **Stage 3**: 20s delay
- **Stage 4**: 40s delay
- **Stage 5**: 80s delay

### 5. PID Guardianship
The technique of managing a unique process identifier (PID) file to ensure that only a single instance of a mission node can occupy an execution slot at any given time.

### 6. Sovereign Tunneling
The management and health-checking of `ngrok` or similar ephemeral tunnels, ensuring the external gateway to the regime remains open during the 120-hour mission window.

---
**PROPERTY OF TRISHULA SOFTWARE — LEVEL 5 SOVEREIGNTY ENFORCED**
