"""
Module pour la gestion de la configuration de la Fourmi de Langton à partir d'un fichier YAML.
"""

import os
import yaml

def lire_configuration():
    """Lit la configuration à partir du fichier config.yaml.

    Returns:
        dict: Le dictionnaire contenant les paramètres de configuration.
    """
    chemin = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
    with open(chemin, 'r', encoding='utf-8') as fichier:
        return yaml.safe_load(fichier)

