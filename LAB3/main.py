import time
import asyncio
from detector_agent import DetectorAgent
from ocr_agent import OCRAgent
from client_agent import ClientAgent


async def run_system():
    # 1. Initialisation des agents
    # Remplace "password" par ton mot de passe par défaut
    detector = DetectorAgent("detector@localhost", "password")
    ocr = OCRAgent("ocr@localhost", "password")
    client = ClientAgent("client@localhost", "password")

    # 2. Configuration du chemin de l'image pour le client
    client.image_path = "C:\\Users\\HP\\PycharmProjects\\TP2_firstsimùpleMAS\\test.jpg"

    # 3. Démarrage des agents
    print("--- Démarrage du système Multi-Agents ---")
    await ocr.start()
    await detector.start()

    # On laisse un petit délai pour que le réseau XMPP s'établisse
    await asyncio.sleep(2)

    # Le client part en dernier pour envoyer l'image
    await client.start()

    # 4. On garde le script en vie pour voir le résultat
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt demandé...")
        await detector.stop()
        await ocr.stop()
        await client.stop()


if __name__ == "__main__":
    asyncio.run(run_system())