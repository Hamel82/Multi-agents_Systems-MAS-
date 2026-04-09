# TP N°1 — Introduction to Multi-Agent Systems

> **Lab Session 1 — JADE & SPADE: Installation and First Agent**  
> Euromed University of Fes — Computer Engineering  
> Author: GOUNGOU Cédric Hamel | Supervisor: Pr Abderrahim Waga  
> Academic Year 2025-2026

---

## Overview

This lab introduces the fundamentals of Multi-Agent Systems (MAS) through two frameworks:

- **Part I — JADE** (Java): Create a first autonomous agent on the JADE platform using IntelliJ IDEA.
- **Part II — SPADE** (Python): Implement a two-agent communication system over XMPP.

---

## Part I — JADE (Java)

### Requirements

- Java 8 or 11 (**Java 9+ module system is incompatible with JADE** — see note below)
- IntelliJ IDEA
- [JADE 4.6](https://jade.tilab.com/) — extract and locate `lib/jade.jar` and `lib/commons-codec.jar`

### Project Structure

```
TP1_JADE/
├── src/
│   └── eu/uemf/agents/
│       └── HelloAgent.java
└── lib/
    ├── jade.jar
    └── commons-codec.jar
```

### Setup in IntelliJ

1. Open IntelliJ → `File > Project Structure > Libraries`
2. Add `jade.jar` and `commons-codec.jar` from the JADE `lib/` folder

>  **Java version fix**: If your project has a `module-info.java` in `src/`, **delete it**.  
> Java 9+ modules break JADE with the error `Could not find or load main class jade.Boot`.  
> Deleting this file forces the project to run as a classic Java application.

### Run Configuration

| Field | Value |
|---|---|
| Main Class | `jade.Boot` |
| Program Arguments | `-gui -local-host 127.0.0.1 -agents myAgent:eu.uemf.agents.HelloAgent` |

- `-gui` — launches the JADE graphical interface (RMA)
- `-local-host 127.0.0.1` — fixes "No ICP active" / communication failure errors
- `-agents name:Class` — creates the agent on startup

### HelloAgent — Source Code

```java
package eu.uemf.agents;

import jade.core.Agent;

public class HelloAgent extends Agent {
    @Override
    protected void setup() {
        System.out.println("Hello World! I am a JADE Agent.");
        System.out.println("My local name is " + getAID().getLocalName());
        System.out.println("My GUID is " + getAID().getName());
    }
}
```

### Expected Output

**Console:**
```
Hello World! I am a JADE Agent.
My local name is myAgent
My GUID is myAgent@127.0.0.1:1099/JADE
```

**JADE GUI (RMA)** shows the Main-Container with three agents:
- `ams` — Agent Management System
- `df` — Directory Facilitator
- `myAgent` — your created agent

---

## Part II — SPADE (Python)

> This part was not required by the lab instructions but was explored as a bonus.

### Requirements

- Python 3.9+
- A public XMPP server account (used: `jabber.hot-chilli.net`)  
  Create two accounts: `mon_agent1_tp1@...` and `mon_agent2_tp1@...`

Install dependencies:

```bash
pip install spade spade_bdi
```

### Implementation

Two agents communicate over XMPP:

- **SenderAgent** — sends a message using a `OneShotBehaviour`
- **ReceiverAgent** — waits up to 10 seconds for an incoming message

```bash
python heloo_agent.py
```

### Technical Observation

The receiver intercepted the XMPP server's automatic welcome message first. By the time the sender's message arrived, the `OneShotBehaviour` had already finished, triggering a `No behaviour matched` warning. This highlights the importance of behaviour lifecycle management in SPADE.

---

## JADE vs SPADE — Quick Comparison

| Criterion | JADE | SPADE |
|---|---|---|
| Language | Java | Python |
| Communication | Internal (Main Container) | External (XMPP server) |
| Agent ID | `AID` — `name@host` | `JID` — `user@xmpp-server` |
| Concurrency | Java Threads | `async/await` (asyncio) |
| AI library support | Limited | Easy (`torch`, `scikit-learn`, etc.) |

---

## Key Concepts

- `setup()` is the agent entry point in both JADE and SPADE (equivalent to `main`)
- `getAID().getLocalName()` / `getAID().getName()` identify the agent locally and globally in JADE
- XMPP ≠ XAMPP — XMPP is an instant messaging protocol; XAMPP is a PHP/MySQL web server stack

---

## License

Academic project — Euromed University of Fes, 2026.
