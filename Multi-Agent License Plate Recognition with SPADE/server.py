from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import time
import asyncio
import logging
from pyjabber.server import Server

# Configuration des logs pour voir ce qui se passe sur le serveur
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main():
    print(" Initialisation du serveur XMPP Pyjabber...")

    # Par défaut, le serveur écoute sur 127.0.0.1 (localhost) et le port 5222
    server = Server()

    # Démarrage du serveur de manière asynchrone
    await server.start()
    print(" Serveur XMPP en ligne ! En attente de la connexion des agents SPADE...")

    # Boucle infinie pour maintenir le serveur actif
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        print("\n Arrêt du serveur XMPP demandé par l'utilisateur.")
        # Ajoute ici une logique d'arrêt propre si pyjabber l'exige,
        # sinon la fermeture du script tuera le processus.


if __name__ == "__main__":
    # Exécution de la boucle asynchrone principale
    asyncio.run(main())