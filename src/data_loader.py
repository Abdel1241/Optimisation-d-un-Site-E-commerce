import pandas as pd
import logging
from config import DATASET_PATH, DOCS 
from pathlib import Path

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class DataLoader:
    """Classe pour charger et explorer les datasets e-commerce"""

    def __init__(self, data_path):
        self.data_path = Path(data_path)  # Utilisation de pathlib pour la gestion des chemins
        if not self.data_path.exists():
            logger.error(f"Le dossier de données {self.data_path} n'existe pas !")
        else:
            logger.info(f"DataLoader initialisé avec le chemin : {self.data_path}")

    def load_data(self, filename):
        """Charge un fichier CSV et retourne un DataFrame"""
        file_path = self.data_path / filename  # Création du chemin complet

        if not file_path.exists():
            logger.error(f"Le fichier {file_path} n'existe pas !")
            return None

        try:
            df = pd.read_csv(file_path)
            logger.info(f"{filename} chargé avec succès ({df.shape[0]} lignes, {df.shape[1]} colonnes) !")
            return df
        except Exception as e:
            logger.error(f"Erreur lors du chargement de {filename} : {e}")
            return None


if __name__ == "__main__":
    data_loader = DataLoader(DATASET_PATH)
    for doc in DOCS:
        doc_df = data_loader.load_data(doc)  # Use the 'doc' variable to specify the filename
        if doc_df is not None:
            print(f"Affichage du DataFrame pour le fichier: {doc}")
            print(doc_df.head())

