from pathlib import Path
from dotenv import load_dotenv
import os

# Définition du chemin du dataset
BASE_DIR = Path.cwd()  # Répertoire actuel
DATASET_PATH = BASE_DIR / ("C:\\Users\\abdel\\Desktop\\Optimisation d'un Site E-commerce\\ecommerce-dataset")# Dossier où sont stockés les fichiers
PROCESSED_DATA_PATH = BASE_DIR / ("C:\\Users\\abdel\\Desktop\\Optimisation d'un Site E-commerce\\processed-ecommerce-dataset") # Dossier où sont stockés les fichiers processed hihi 
DOCS = ["events.csv", "item_properties_part1.csv", "item_properties_part2.csv", "category_tree.csv"]
PROCESSED_DOCS =["events_processed.csv", "item_properties_processed.csv", "category_tree_processed.csv"]
EXPORTS_DATA_PATH = os.path.join(BASE_DIR, "exports_excel")

# Fichiers de données
EVENTS_FILE = DATASET_PATH / "events.csv"
ITEM_PROPERTIES_FILE1 = DATASET_PATH / "item_properties_part1.csv"
ITEM_PROPERTIES_FILE2 = DATASET_PATH / "item_properties_part2.csv"
CATEGORY_TREE_FILE = DATASET_PATH / "category_tree.csv"

# Paramètres globaux
RANDOM_SEED = 42
TEST_SIZE = 0.2

print(f"📂 Chemin des fichiers de données : {DATASET_PATH}")
print(f"📄 Fichier events : {EVENTS_FILE}")
print(f"📄 Fichier properties 1 : {ITEM_PROPERTIES_FILE1}")
print(f"📄 Fichier properties 2 : {ITEM_PROPERTIES_FILE2}")
print(f"📄 Fichier catégories : {CATEGORY_TREE_FILE}")
