# DockerManager Discord : 

Un bot discord qui vous permet de gérer vos container à travers un tunel SSH depuis discord.

## Prérequis : 

- Un serveur `openssh` sur votre machine avec `docker` d'installer.
- Python3 sur le machine qui héberge le bot.
- Un compte et un serveur discord dont vous avez récupérer l'id.
- Un token pour un bot discord. 

## Setup initial :

- Installer les bibliothèques requises : `pip install -r requirements.txt`.
- Remplir le fichier .env avec vos informations de connexion (TOKEN, ip...)
- Démarrer le fichier `main.py` : `python3 main.py`

## Comment l'utiliser ? 

Saississez `/` dans un des salons de votre serveur pour découvrir la liste des commandes.