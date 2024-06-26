import logging
import os
from logging.handlers import RotatingFileHandler

# Créer un répertoire pour les journaux s'il n'existe pas
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)

# Chemin du fichier de journalisation
log_file = os.path.join(log_directory, "app.log")

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Niveau global du logger

# Gestionnaire pour l'affichage dans la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Gestionnaire pour l'écriture dans un fichier avec rotation
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
file_handler.setLevel(logging.INFO)

# Format du message de journalisation
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Associer le format au gestionnaire
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Ajouter les gestionnaires au logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Exemple d'utilisation
logger.debug("Ceci est un message de débogage.")
logger.info("Ceci est un message d'information.")
logger.warning("Ceci est un message d'avertissement.")
logger.error("Ceci est un message d'erreur.")
logger.critical("Ceci est un message critique.")

# Exemple de gestion d'une exception avec journalisation
try:
    1 / 0
except ZeroDivisionError as e:
    logger.exception("Une exception s'est produite : %s", e)
