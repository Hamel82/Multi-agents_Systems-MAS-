# License Plate Recognition — Multi-Agent System (SPADE)

> **MAS Lab — SPADE / Python**  
> Euromed University of Fes | Author: GOUNGOU Cédric Hamel | Supervisor: Pr Abderrahim WAGA

---

## What it does

Three agents work together in a pipeline to detect and read a license plate from an image:

```
ClientAgent  →[image]→  DetectorAgent  →[plate crop]→  OCRAgent  →[text]→  ClientAgent
```

---

## Agents

| Agent | JID | Role |
|---|---|---|
| **ClientAgent** | `client@localhost` | Sends the image, receives the result |
| **DetectorAgent** | `detector@localhost` | Detects the plate with YOLOv8, sends the crop |
| **OCRAgent** | `ocr@localhost` | Reads the plate text with EasyOCR |

---

## Requirements

```bash
pip install spade pyjabber ultralytics easyocr opencv-python numpy
```

- GPU recommended (CUDA) — both DetectorAgent and OCRAgent fall back to CPU automatically
- Place `license_plate_detector.pt` in the project root
- Update `image_path` in `main.py` and `client_agent.py` to point to your test image

---

## How to run

**Terminal 1 — start the XMPP server first:**
```bash
python server.py
```

**Terminal 2 — start the agents:**
```bash
python main.py
```

---

## Expected output

```
--- Démarrage du système Multi-Agents ---
 OCR: EasyOCR prêt avec CUDA 
 Detector: Modèle chargé sur GPU (CUDA)
 Client: Image 'test.jpg' envoyée au serveur.
 Detector: Plaque détectée [84,56,231,104] et envoyée à l'OCR.
 [RÉSULTAT FINAL] Plaque identifiée : GYI2 RZB
 RÉSULTAT REÇU PAR LE CLIENT : GYI2 RZB
```

---

## Project structure

```
├── main.py              # Starts all agents
├── server.py            # Embedded XMPP server (pyjabber)
├── client_agent.py      # Sends image, receives OCR result
├── detector_agent.py    # YOLOv8 plate detection
├── ocr_agent.py         # EasyOCR text recognition
├── protocol.py          # Shared JIDs and message type constants
└── license_plate_detector.pt  # YOLOv8 model weights
```

---

## Notes

- The server must be running **before** `main.py` — agents register on XMPP at startup
- `main.py` waits 2 seconds after starting OCR and Detector before launching the Client, to let them register on the XMPP network
- Images are transmitted as Base64-encoded strings inside XMPP message bodies
- Stop with `Ctrl+C`
