
# src/__init__.py

"""
Module principal pour l'optimisation du site e-commerce.
"""

# Importation des modules principaux
from .config import *
from .data_loader import load_data
from .data_processing import clean_data
from .optimiser import ab_test_analysis
from .utils import setup_logger

# Initialisation du logger
logger = setup_logger()
logger.info("Module d'optimisation e-commerce initialisé.")
