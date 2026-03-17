from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import cv2
import base64
import os
import protocol

class ClientAgent(Agent):
    # On définit l'image_path comme un attribut de classe ou d'instance après l'init
    image_path = "C:\\Users\\HP\\PycharmProjects\\TP2_firstsimùpleMAS\\test.jpg"

    class SendImageBehaviour(OneShotBehaviour):
        async def run(self):
            # 1. Vérification si le fichier existe
            if not os.path.exists(self.agent.image_path):
                print(f" Client: Erreur, le fichier {self.agent.image_path} n'existe pas.")
                return

            # 2. Lecture de l'image
            image = cv2.imread(self.agent.image_path)
            if image is None:
                print(" Client: Impossible de lire l'image (format invalide ?).")
                return

            # 3. Encodage en Base64
            _, img_encoded = cv2.imencode('.jpg', image)
            img_b64 = base64.b64encode(img_encoded).decode('utf-8')

            # 4. Création du message
            msg = Message(to=protocol.DETECTOR_JID)
            msg.set_metadata("performative", "request")
            msg.set_metadata("type", protocol.TYPE_IMAGE_FULL)
            msg.body = img_b64

            # 5. Envoi
            await self.send(msg)
            print(f" Client: Image '{self.agent.image_path}' envoyée au serveur.")

    class ReceiveResultBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=30)
            if msg and msg.metadata.get("type") == protocol.TYPE_OCR_RESULT:
                print(f"🏆 RÉSULTAT REÇU PAR LE CLIENT : {msg.body}")

    async def setup(self):
        print(f"Client Agent démarré ({self.jid})")
        self.add_behaviour(self.SendImageBehaviour())
        self.add_behaviour(self.ReceiveResultBehaviour())