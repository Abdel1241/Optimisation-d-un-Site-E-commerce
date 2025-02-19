import kaggle 
import os

os.system("kaggle datasets download -d retailrocket/ecommerce-dataset")

import zipfile

# Définir le chemin du fichier ZIP
zip_path = "ecommerce-dataset.zip"

# Extraire les fichiers
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall("ecommerce_data")

print("Extraction terminée !")
