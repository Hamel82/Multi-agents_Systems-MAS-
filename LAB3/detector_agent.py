from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import protocol


class DetectorAgent(Agent):
    # On passe le model_path au setup via un attribut si besoin,
    # mais on peut aussi le mettre en dur ou en variable d'agent.
    model_path = "C:\\Users\\HP\\PycharmProjects\\TP2_firstsimùpleMAS\\license_plate_detector.pt"

    class DetectPlateBehaviour(CyclicBehaviour):
        async def on_start(self):
            # On charge le modèle UNE SEULE FOIS au démarrage du comportement
            # .to('cuda') active ton GPU
            try:
                self.model = YOLO(self.agent.model_path).to('cuda')
                print(f" Detector: Modèle chargé sur GPU (CUDA)")
            except Exception as e:
                print(f" Detector: Erreur CUDA, passage sur CPU: {e}")
                self.model = YOLO(self.agent.model_path)

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.metadata.get("type") == protocol.TYPE_IMAGE_FULL:
                try:
                    # 1. Décodage de l'image reçue du Client
                    img_bytes = base64.b64decode(msg.body)
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if image is None:
                        print(" Detector: Erreur de décodage de l'image.")
                        return

                    # 2. Détection (conf=0.5 pour éviter les faux positifs)
                    results = self.model(image, conf=0.5)

                    found = False
                    for result in results:
                        for box in result.boxes:
                            found = True
                            # Récupération des coordonnées
                            x1, y1, x2, y2 = map(int, box.xyxy[0])

                            # 3. Crop de la plaque
                            plate = image[y1:y2, x1:x2]

                            # 4. Encodage en base64 pour l'envoi
                            _, img_encoded = cv2.imencode('.jpg', plate)
                            plate_b64 = base64.b64encode(img_encoded).decode('utf-8')

                            # 5. Envoi à l'OCR au serveur
                            reply = Message(to=protocol.OCR_JID)
                            reply.set_metadata("performative", "request")
                            reply.set_metadata("type", protocol.TYPE_PLATE_CROP)
                            reply.body = plate_b64
                            await self.send(reply)
                            print("✅ Detector: Plaque envoyée à l'OCR.")
                            print(f" Detector: Plaque détectée [{x1},{y1},{x2},{y2}] et envoyée à l'OCR.")

                    if not found:
                        print(" Detector: Aucune plaque détectée sur cette image.")

                except Exception as e:
                    print(f" Detector: Erreur lors du traitement : {e}")

    async def setup(self):
        print(f"Agent Détecteur en cours de démarrage ({self.jid})...")
        self.add_behaviour(self.DetectPlateBehaviour())