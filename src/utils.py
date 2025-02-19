import logging
from pathlib import Path

def setup_logger(log_file="ecommerce.log"):
    """Configure un logger pour l'application."""
    logger = logging.getLogger("EcommerceLogger")
    
    # Évite d'ajouter plusieurs handlers si le logger existe déjà
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Format des logs
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Handler pour l'affichage dans la console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        # Handler pour écrire dans un fichier log
        log_path = Path(log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger

# Exemple d'utilisation
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Le logger fonctionne correctement !")
    logger.warning("Ceci est un avertissement.")
    logger.error("Ceci est une erreur.")
