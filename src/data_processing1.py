import pandas as pd
import logging
from pathlib import Path
from data_loader import DataLoader

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class DataProcessing:
    """Classe pour prétraiter et sauvegarder les données d'e-commerce."""

    def __init__(self, datasets, data_path, processed_path, force_preprocessing=False):
        """
        Initialise l'objet DataProcessing avec les datasets à traiter.
        Args:
            datasets (list or str): Liste des fichiers à charger.
            data_path (str): Chemin vers le dossier contenant les fichiers bruts.
            processed_path (str): Chemin vers le dossier où sauvegarder les fichiers prétraités.
            force_preprocessing (bool): Forcer le retraitement même si les fichiers existent déjà.
        """
        self.datasets = [datasets] if isinstance(datasets, str) else datasets
        self.data_loader = DataLoader(data_path)
        self.processed_path = Path(processed_path)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.force_preprocessing = force_preprocessing  # Option pour forcer le retraitement

    def remove_duplicates(self, df, dataset_name):
        """
        Supprime les doublons d'un DataFrame et affiche le nombre de lignes avant/après.
        """
        initial_rows = len(df)
        df = df.drop_duplicates()
        final_rows = len(df)
        logger.info(f"{dataset_name}: {initial_rows - final_rows} doublons supprimés ({initial_rows} → {final_rows} lignes).")
        return df

    def save_processed_data(self, data, dataset_name):
        """
        Sauvegarde les données prétraitées dans un fichier CSV.
        """
        file_path = self.processed_path / (f"{dataset_name}_processed.csv" if not dataset_name.endswith(".csv") else dataset_name.replace(".csv", "_processed.csv"))
        data.to_csv(file_path, index=False)
        logger.info(f"{dataset_name}: Données sauvegardées ({len(data)} lignes) dans {file_path}")

            
    def load_processed_data(self, dataset_name):
        """
        Charge les données prétraitées si elles existent et si le mode force_preprocessing est désactivé.
        """
        file_path = self.processed_path / (f"{dataset_name}_processed.csv" if not dataset_name.endswith(".csv") else dataset_name.replace(".csv", "_processed.csv"))
        if file_path.exists() and not self.force_preprocessing:
            logger.info(f"{dataset_name}: Chargement des données prétraitées existantes.")
            return pd.read_csv(file_path)
        return None


    def preprocess_items(self):
        """Fusionne les fichiers item_properties_part1 et item_properties_part2, supprime les doublons et convertit les timestamps."""
        df1 = self.data_loader.load_data("item_properties_part1.csv")
        df2 = self.data_loader.load_data("item_properties_part2.csv")

        if df1 is not None and df2 is not None:
            initial_total_rows = len(df1) + len(df2)
            items_combined = pd.concat([df1, df2])
            logger.info(f"item_properties: Fusion de 2 fichiers ({len(df1)} + {len(df2)}) → {len(items_combined)} lignes avant nettoyage.")

            items_cleaned = self.remove_duplicates(items_combined, "item_properties")

            if "timestamp" in items_cleaned.columns:
                items_cleaned["timestamp"] = pd.to_datetime(items_cleaned["timestamp"], unit="ms")

            logger.info("item_properties: Fusion et nettoyage terminés.")
            return items_cleaned
        else:
            logger.warning("Les fichiers item_properties_part1.csv et item_properties_part2.csv sont introuvables.")
            return None

    def preprocess_categories(self):
        """Charge et nettoie les catégories des articles."""
        df = self.data_loader.load_data("category_tree.csv")
        if df is not None:
            df = self.remove_duplicates(df, "category_tree")
            logger.info("category_tree: Prétraitement terminé.")
            return df
        return None

    def preprocess_events(self):
        """Charge les événements, supprime les doublons et convertit les timestamps."""
        df = self.data_loader.load_data("events.csv")

        if df is not None:
            df = self.remove_duplicates(df, "events")

            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            logger.info("events: Prétraitement terminé.")
            return df
        return None

    def preprocess_data(self):
        """
        Exécute les prétraitements et enregistre les résultats.
        """
        processed_data = {}

        processing_map = {
            "events.csv": self.preprocess_events,
            "category_tree.csv": self.preprocess_categories,
            "item_properties": self.preprocess_items,
        }

        for dataset in self.datasets:
            key = "item_properties" if "item_properties" in dataset else dataset
            try:
                # Vérifie si le fichier a déjà été prétraité
                existing_data = self.load_processed_data(key)
                if existing_data is not None:
                    processed_data[key] = existing_data
                elif key in processing_map:
                    processed = processing_map[key]()
                    if processed is not None:
                        self.save_processed_data(processed, key)
                        processed_data[key] = processed
                else:
                    logger.warning(f"Aucune méthode de prétraitement définie pour {key}.")
            except Exception as e:
                logger.error(f"Erreur lors du traitement du dataset {key} : {e}")

        logger.info("✅ Prétraitement terminé pour tous les fichiers.")
        return processed_data


if __name__ == "__main__":
    # Exécution du prétraitement avec option pour forcer ou non
    data_processor = DataProcessing(
        ["events.csv", "item_properties_part1.csv", "item_properties_part2.csv", "category_tree.csv"],
        data_path="ecommerce-dataset",
        processed_path="processed-ecommerce-dataset",
        force_preprocessing=True  #  Change à False si tu veux utiliser les fichiers existants
    )
    
    processed_data = data_processor.preprocess_data()
