from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import cv2
import easyocr
import numpy as np
import base64
import protocol


class OCRAgent(Agent):
    class ReadPlateBehaviour(CyclicBehaviour):
        async def on_start(self):
            # Initialisation du Reader avec support GPU (gpu=True)
            # On le met dans on_start pour ne pas bloquer le setup de l'agent
            print(" OCR: Chargement d'EasyOCR sur GPU...")
            try:
                self.reader = easyocr.Reader(['en'], gpu=True)
                print(" OCR: EasyOCR prêt avec CUDA ✅")
            except Exception as e:
                print(f" OCR: Erreur GPU, utilisation du CPU : {e}")
                self.reader = easyocr.Reader(['en'], gpu=False)

        async def run(self):
            # On attend le message du DetectorAgent
            msg = await self.receive(timeout=10)
            if msg and msg.metadata.get("type") == protocol.TYPE_PLATE_CROP:
                try:
                    # 1. Décodage de la petite image (crop) reçue en Base64
                    img_bytes = base64.b64decode(msg.body)
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    plate_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if plate_img is None:
                        print(" OCR: Image de plaque corrompue.")
                        return

                    # 2. Lecture du texte
                    # detail=0 permet d'avoir juste le texte sans les coordonnées
                    print()
                    results = self.reader.readtext(plate_img, detail=0)

                    if results:
                        # On nettoie et on concatène le texte trouvé
                        text = " ".join(results).upper().strip()
                        print(f" [RÉSULTAT FINAL] Plaque identifiée : {text}")

                        # RENVOI AU CLIENT
                        reply = Message(to=protocol.CLIENT_JID)
                        reply.set_metadata("performative", "inform")
                        reply.set_metadata("type", protocol.TYPE_OCR_RESULT)
                        reply.body = text
                        await self.send(reply)
                        print(f" OCR: Texte '{text}' renvoyé au Client.")

                    else:
                        print("OCR: Aucune plaque lisible sur l'image reçue.")

                except Exception as e:
                    print(f" OCR: Erreur lors de l'analyse : {e}")

    async def setup(self):
        print(f"Agent OCR en cours de démarrage ({self.jid})...")
        self.add_behaviour(self.ReadPlateBehaviour())