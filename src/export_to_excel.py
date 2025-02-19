import os
import logging
import pandas as pd
from config import PROCESSED_DOCS
from config import PROCESSED_DATA_PATH
from config import EXPORTS_DATA_PATH

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


os.makedirs(EXPORTS_DATA_PATH, exist_ok=True)

# Nombre maximum de lignes par fichier Excel
MAX_ROWS = 10_000_000

def export_to_excel():
    """
    Charge et exporte tous les fichiers listés dans PROCESSED_DOCS vers des fichiers Excel.
    Si un fichier dépasse la limite de 1 000 000 lignes, il est fractionné en plusieurs fichiers.
    """
    exported_files = []
    
    for filename in PROCESSED_DOCS:
        filepath = os.path.join(PROCESSED_DATA_PATH, filename)
        
        if os.path.exists(filepath):
            try:
                # Chargement des données
                df = pd.read_csv(filepath)
                export_filename = filename.replace(".csv", ".xlsx")
                export_filepath = os.path.join(EXPORTS_DATA_PATH, export_filename)

                if len(df) > MAX_ROWS:
                    logger.warning(f"⚠️ {filename} est trop volumineux ({len(df)} lignes). Fractionnement en plusieurs fichiers.")
                    
                    part = 1
                    for i in range(0, len(df), MAX_ROWS):
                        chunk = df.iloc[i:i+MAX_ROWS]  # Découpe le dataframe
                        chunk_filename = export_filename.replace(".xlsx", f"_part{part}.xlsx")
                        chunk_filepath = os.path.join(EXPORTS_DATA_PATH, chunk_filename)
                        chunk.to_excel(chunk_filepath, index=False, engine="openpyxl")
                        logger.info(f"✅ Partie {part} de {filename} exportée vers {chunk_filepath}")
                        exported_files.append(chunk_filepath)
                        part += 1
                
                else:
                    df.to_excel(export_filepath, index=False, engine="openpyxl")
                    logger.info(f"✅ {filename} exporté vers {export_filepath}")
                    exported_files.append(export_filepath)

            except Exception as e:
                logger.error(f"❌ Erreur lors de l'export de {filename} : {e}")
        else:
            logger.error(f"⚠️ Fichier {filename} introuvable, non exporté.")

    return exported_files

# Exécution du script
if __name__ == "__main__":
    exported_files = export_to_excel()
    
    if exported_files:
        logger.info("📂 Tous les fichiers ont été exportés avec succès dans le dossier 'exports_excel' !")
    else:
        logger.warning("❌ Aucun fichier n'a été exporté.")
