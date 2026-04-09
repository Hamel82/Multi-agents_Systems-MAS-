# Multi-Agent Systems with SPADE — FIPA-ACL Communication

**Student:** GOUNGOU Hamel  
**Framework:** SPADE (Smart Python Agent Development Environment)  
**Protocol:** FIPA-ACL (Foundation for Intelligent Physical Agents)  
**XMPP Server:** PyJabber (embedded Python server)  
**Date:** March 30, 2026

---

## Overview

This practical work implements three major families of FIPA-ACL performatives in a real multi-agent system using the SPADE framework. Agents communicate over a local XMPP server (PyJabber) using standardised message types.

| Exercise | Protocol | Agents involved |
|----------|----------|-----------------|
| Exercise 1 | QUERY-IF / INFORM | `SensorAgent`, `MonitorAgent` |
| Exercise 2 | REQUEST / AGREE / REFUSE / FAILURE | `RobotAgent`, `MonitorAgentEx2` |
| Exercise 3 | CFP / PROPOSE / ACCEPT-PROPOSAL / REJECT-PROPOSAL | `WorkerAgent` ×2, `MonitorAgentEx3` |

---

## Project Structure

```
.
├── server.py           # Embedded PyJabber XMPP server
├── main.py             # Entry point — run all exercises here
│
├── sensor_agent.py     # Exercise 1 — Sensor (responds to QUERY-IF with INFORM)
├── monitor_agent.py    # Exercise 1 — Monitor (sends QUERY-IF, waits for INFORM)
│
├── robot_agent.py      # Exercise 2 — Robot (evaluates battery, AGREE/REFUSE/FAILURE)
├── monitor_ex2.py      # Exercise 2 — Monitor (sends 5 REQUEST orders)
│
├── worker_agent.py     # Exercise 3 — Worker (responds to CFP with PROPOSE)
├── monitor_ex3.py      # Exercise 3 — Monitor (CFP, selects cheapest proposal)
│
└── pyjabber.db         # PyJabber local XMPP database (auto-generated)
```

---

## Prerequisites

- Python 3.9+
- Install dependencies:

```bash
pip install spade pyjabber
```

---

## Running the Project

### Step 1 — Start the XMPP Server

Open a first terminal and run:

```bash
python server.py
```

Wait for the message `Serveur XMPP en ligne !` before proceeding.

### Step 2 — Run an Exercise

Open a second terminal and run `main.py`. By default, **Exercise 3** is active. To switch exercises, edit `main.py` and uncomment the block corresponding to the exercise you want to run (Exercise 1 and 2 blocks are wrapped in triple-quoted strings).

```bash
python main.py
```

---

## Exercises

### Exercise 1 — Information Exchange (QUERY-IF / INFORM)

**Scenario:** A Monitor Agent queries a Sensor Agent about the current temperature. The Sensor only responds to `query-if` messages thanks to a strict FIPA-ACL Template.

**Communication flow:**
```
Monitor  --[QUERY-IF]-->  Sensor
Sensor   --[INFORM]---->  Monitor
```

**Key agents:**
- `SensorAgent` (`sensor_agent.py`) — uses a `CyclicBehaviour` to stay permanently available; filters incoming messages with a `query-if` Template.
- `MonitorAgent` (`monitor_agent.py`) — uses a `OneShotBehaviour` to send one query and wait for the reply.

**Expected output:**
```
[Monitor] QUERY-IF sent.
[Sensor] Request received: What is the current temperature?
[Sensor] Reply (INFORM) sent.
[Monitor] Response received: The temperature is 25 C
```

---

### Exercise 2 — Action Directives (REQUEST / AGREE / REFUSE / FAILURE)

**Scenario:** A Monitor Agent sends 5 successive movement orders to an autonomous Robot Agent. The Robot evaluates its battery level before accepting or refusing each order.

**Decision logic:**

| Movement | Position | Battery | Result |
|----------|----------|---------|--------|
| #1 | (5, 3) | 80% | AGREE + INFORM (success) |
| #2 | (8, 1) | 65% | AGREE + FAILURE (obstacle) |
| #3 | (2, 6) | 50% | AGREE + INFORM (success) |
| #4 | (4, 4) | 35% | AGREE + INFORM (success) |
| #5 | (9, 2) | 20% | REFUSE (battery too low) |

**Communication flow:**
```
Monitor  --[REQUEST]-->  Robot
Robot    --[AGREE]----->  Monitor   (if battery > 20%)
Robot    --[INFORM]---->  Monitor   (movement succeeded)
         or
Robot    --[FAILURE]--->  Monitor   (obstacle encountered)
         ---
Robot    --[REFUSE]---->  Monitor   (if battery <= 20%)
```

**Key agents:**
- `RobotAgent` (`robot_agent.py`) — started with `battery_level=80`; decreases by 15% per movement; obstacle is hardcoded on movement #2.
- `MonitorAgentEx2` (`monitor_ex2.py`) — sends the 5 predefined `REQUEST` messages sequentially, waits for `AGREE`/`REFUSE`, then for `INFORM`/`FAILURE` if agreed.

**Expected output (abbreviated):**
```
[Monitor] Sending REQUEST #1: Move to position (5, 3)
[Monitor] Response #1 (AGREE): Movement #1 authorized. Execution in progress.
[Monitor] Result #1 (INFORM): Movement #1 completed successfully. Battery: 65%
...
[Monitor] Response #5 (REFUSE): Movement #5 refused: battery too low (20%).
[Monitor] All movement requests completed.
```

---

### Exercise 3 — Contract Net Negotiation (CFP / PROPOSE / ACCEPT / REJECT)

**Scenario:** A Monitor Agent must delegate a CNN Training task to one of two Worker Agents. It broadcasts a Call For Proposals (CFP), collects bids, and selects the cheapest worker.

**Communication flow:**
```
Monitor  --[CFP]---------------->  Worker1 (cost: 10 units)
Monitor  --[CFP]---------------->  Worker2 (cost:  5 units)
Worker1  --[PROPOSE 10 units]-->  Monitor
Worker2  --[PROPOSE  5 units]-->  Monitor
Monitor  --[ACCEPT-PROPOSAL]--->  Worker2  (cheapest)
Monitor  --[REJECT-PROPOSAL]--->  Worker1
```

**Key agents:**
- `WorkerAgent` (`worker_agent.py`) — instantiated with a `cost` parameter; uses two separate behaviours (one for `cfp`, one for `accept-proposal | reject-proposal`) with distinct Templates.
- `MonitorAgentEx3` (`monitor_ex3.py`) — broadcasts CFP, collects all proposals, sorts by cost, sends `accept-proposal` to the winner and `reject-proposal` to the rest.

**Expected output:**
```
[Monitor] CFP sent to worker1@localhost
[Monitor] CFP sent to worker2@localhost
[Worker worker1] PROPOSE sent — Cost: 10 time units
[Worker worker2] PROPOSE sent — Cost: 5 time units
[Monitor] ACCEPT-PROPOSAL sent to worker2@localhost
[Monitor] REJECT-PROPOSAL sent to worker1@localhost
[Worker worker2] Decision received: ACCEPT-PROPOSAL
[Worker worker1] Decision received: REJECT-PROPOSAL
```

---

## Architecture Notes

- **FIPA-ACL Templates** — every agent uses `Template` objects with `set_metadata("performative", ...)` to filter incoming messages. This ensures agents only process messages intended for them and avoids cross-exercise interference.
- **Behaviour types** — `OneShotBehaviour` is used for one-time actions (Monitor sending a single query or CFP round); `CyclicBehaviour` is used for agents that must remain permanently listening (Sensor, Robot, Worker).
- **Template OR operator** — in `worker_agent.py`, the `|` operator combines two Templates so a single `BehaviorDecision` behaviour listens for both `accept-proposal` and `reject-proposal`.
- **XMPP transport** — all messages are routed through the local PyJabber server on `localhost`. Agents are registered with JIDs of the form `agentname@localhost`.

---

## Switching Between Exercises

In `main.py`, each exercise block is delimited by triple-quoted strings (`""" ... """`). To activate a specific exercise:

1. Wrap the currently active block in `""" ... """`.
2. Remove the `""" ... """` from the block you want to run.

Only one exercise should be active at a time to avoid JID conflicts on the XMPP server.
