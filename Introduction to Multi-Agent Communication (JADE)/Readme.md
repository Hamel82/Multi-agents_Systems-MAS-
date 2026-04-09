# TP N°2 — ACL Communication Between Agents (JADE)

> **Lab Session 2 — Multi-Agent Systems: ACL Message Exchange**  
> Euromed University of Fes — Computer Engineering  
> Author: GOUNGOU Cédric Hamel | Supervisor: Pr Abderrahim Waga  
> Academic Year 2025-2026

---

## Overview

This lab covers the fundamentals of inter-agent communication using **ACL (Agent Communication Language)** in the JADE framework. Four exercises build progressively from a simple one-way message to a full multi-agent negotiation protocol.

---

## Project Structure

```
src/eu/uemf/agents/
├── AgentA.java          # Exercises 1 & 2 — Sender agent (INFORM / REQUEST)
├── AgentB.java          # Exercises 1 & 2 — Receiver agent
├── CoordinatorAgent.java  # Exercise 3 — Sends requests to two experts
├── Expert1.java         # Exercise 3 — Expert agent #1
├── Expert2.java         # Exercise 3 — Expert agent #2
├── Buyer.java           # Exercise 4 — Negotiation initiator (CFP)
├── seller1.java         # Exercise 4 — Seller agent #1 (price: 500)
├── seller2.java         # Exercise 4 — Seller agent #2 (price: 450)
└── HelloAgent.java      # Carried over from TP1
```

> **Note:** `AgentA.java` and `AgentB.java` contain both Exercise 1 and Exercise 2 implementations. The active version is uncommented; the other is commented out. Switch between them as needed.

---

## Requirements

- Java 8 or 11 (Java 9+ modules are incompatible with JADE — delete `module-info.java` if present)
- IntelliJ IDEA
- JADE 4.6 — add `jade.jar` and `commons-codec.jar` to the project libraries

---

## Run Configuration (all exercises)

| Field | Value |
|---|---|
| Main Class | `jade.Boot` |
| Program Arguments | see each exercise below |

---

## Exercise 1 — Unidirectional Communication

**Pattern:** `AgentA` → `INFORM` → `AgentB`

AgentA sends a single `INFORM` message via `OneShotBehaviour`. AgentB listens indefinitely with a `CyclicBehaviour` and prints any incoming message. No reply is sent.

**Run arguments:**
```
-gui -local-host 127.0.0.1 -agents agent1:eu.uemf.agents.AgentB;agentA:eu.uemf.agents.AgentA
```

**Expected output:**
```
agentA started and will send a message...
agentA sent message to agentB
agent1 received message:
From: agentA
Content: Hello B!
```

**Key points:**
- `OneShotBehaviour` executes once — suitable for a single send.
- `CyclicBehaviour` loops indefinitely listening for messages.
- Call `block()` when `msg == null` to avoid a CPU busy-wait.

---

## Exercise 2 — Bidirectional Communication

**Pattern:** `AgentA` → `REQUEST` → `AgentB` → `INFORM` (reply) → `AgentA`

AgentA sends a `REQUEST` then switches to listening mode. AgentB checks the performative, uses `createReply()` to generate a correctly addressed reply, and sends an `INFORM` back.

**Run arguments:**
```
-gui -local-host 127.0.0.1 -agents agent1:eu.uemf.agents.AgentB;agentA:eu.uemf.agents.AgentA
```

> Uncomment the Exercise 2 block in both `AgentA.java` and `AgentB.java` before running.

**Expected output:**
```
agentA sent message to agentB
agentA waiting for response...
agent1 received: REQUEST -- What is the temperature?
agent1 sent reply to agentA
agentA received: INFORM -- It is 25°C.
```

**Key points:**
- `createReply()` automatically copies `conversation-id` and `reply-to` metadata.
- Checking `getPerformative()` lets an agent filter only relevant messages.
- AgentA uses two separate behaviours: one for sending, one for receiving.

---

## Exercise 3 — 3-Agent Coordination (1 → 2)

**Pattern:** `CoordinatorAgent` → `REQUEST` × 2 → `Expert1`, `Expert2` → `INFORM` × 2 → `CoordinatorAgent`

The coordinator sends a `REQUEST` to each expert via `OneShotBehaviour`, then listens with a `CyclicBehaviour` using a counter. When both `INFORM` replies are received (counter == 2), it prints the global result and removes its listener behaviour.

**Run arguments:**
```
-gui -local-host 127.0.0.1 -agents agent1:eu.uemf.agents.Expert1;agent2:eu.uemf.agents.Expert2;coordinator:eu.uemf.agents.CoordinatorAgent
```

**Expected output:**
```
coordinator sent messages to Expert1 and Expert2
agent1 received: REQUEST -- Hello B!
agent2 received: REQUEST -- Hello C!
agent1 sent reply to coordinator
agent2 sent reply to coordinator
coordinator received INFORM from agent1 | Counter = 1
coordinator received INFORM from agent2 | Counter = 2
========================================
GLOBAL RESULT: All replies completed!
Total INFORM received: 2
========================================
coordinator: Listener behaviour removed.
```

**Key points:**
- An instance counter tracks how many replies have arrived.
- `myAgent.removeBehaviour(this)` cleanly stops the listener once coordination is done.
- `OneShotBehaviour` and `CyclicBehaviour` run in parallel within JADE's internal scheduler.
- Expert1 and Expert2 are structurally identical — in practice a single parameterised class would suffice.

---

## Exercise 4 — Decision Making & Negotiation

**Pattern:** `Buyer` → `CFP` × 2 → `Seller1`, `Seller2` → `PROPOSE` × 2 → `Buyer` → `ACCEPT_PROPOSAL` + `REJECT_PROPOSAL`

The Buyer issues a Call For Proposal (CFP) to both sellers. Each seller replies with a `PROPOSE` containing its price. The Buyer collects both proposals, compares prices, sends `ACCEPT_PROPOSAL` to the cheapest and `REJECT_PROPOSAL` to the other, then stops its listener.

**Run arguments:**
```
-gui -local-host 127.0.0.1 -agents seller1:eu.uemf.agents.seller1;seller2:eu.uemf.agents.seller2;buyer:eu.uemf.agents.Buyer
```

**Agent prices (hardcoded):**

| Agent | Price |
|---|---|
| seller1 | 500 |
| seller2 | 450 |

**Expected output:**
```
buyer (Buyer) started...
seller1 started with price: 500
seller2 started with price: 450
buyer sent CFP to Seller1
buyer sent CFP to Seller2
seller1 received CFP from buyer => sent PROPOSE: 500
seller2 received CFP from buyer => sent PROPOSE: 450
buyer received PROPOSE from seller1 with price: 500
buyer received PROPOSE from seller2 with price: 450
========================================
Comparison:
  Seller1 price: 500
  Seller2 price: 450
  Winner: seller2 with price 450
========================================
buyer sent ACCEPT_PROPOSAL to seller2
buyer sent REJECT_PROPOSAL to seller1
seller2: Hooray, I won the deal! Price = 450
seller1: Sorry, I lost the deal. Better luck next time!
buyer: Decision made, listener stopped.
```

**Key points:**
- `MessageTemplate.MatchPerformative()` filters messages by type, avoiding unrelated message processing.
- `Integer.MAX_VALUE` as initial best price ensures the first proposal always becomes the reference.
- `blockingReceive(template)` in sellers suspends the agent until a matching message arrives — no busy-wait.
- Prices can be passed as JADE agent arguments at startup to make sellers configurable without recompilation.

---

## ACL Performatives Used

| Performative | Meaning | Used in |
|---|---|---|
| `INFORM` | Share information | Ex. 1, 2, 3 |
| `REQUEST` | Request an action | Ex. 2, 3 |
| `CFP` | Call For Proposal | Ex. 4 |
| `PROPOSE` | Submit a proposal | Ex. 4 |
| `ACCEPT_PROPOSAL` | Accept a proposal | Ex. 4 |
| `REJECT_PROPOSAL` | Reject a proposal | Ex. 4 |

---

## License

Academic project — Euromed University of Fes, 2026.
