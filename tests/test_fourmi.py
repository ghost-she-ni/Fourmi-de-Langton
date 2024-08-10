"""
Tests unitaires pour la simulation de la Fourmi de Langton.
"""

import unittest
import sys
import os

# Ajouter le chemin du projet pour permettre l'importation correcte des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Les importations des modules du projet doivent venir après la configuration du chemin
from fourmi.grille import Grille
from fourmi.fourmi import Fourmi

class TestFourmiDeLangton(unittest.TestCase):
    """Tests pour les classes Grille et Fourmi de la simulation de la Fourmi de Langton."""

    def test_grille_initialisation(self):
        """Test de l'initialisation de la grille."""
        grille = Grille(5, 5)
        self.assertEqual(grille.largeur, 5)
        self.assertEqual(grille.hauteur, 5)
        for ligne in grille.grille:
            self.assertEqual(ligne, [0, 0, 0, 0, 0])

    def test_changer_couleur_case(self):
        """Test du changement de couleur d'une case."""
        grille = Grille(3, 3)
        grille.changer_couleur_case(1, 1)
        self.assertEqual(grille.obtenir_couleur_case(1, 1), 1)
        grille.changer_couleur_case(1, 1)
        self.assertEqual(grille.obtenir_couleur_case(1, 1), 0)

    def test_fourmi_mouvement(self):
        """Test du mouvement de la fourmi sur la grille."""
        fourmi = Fourmi(1, 1, 0)
        grille = Grille(3, 3)
        # La fourmi devrait tourner à droite sur une case blanche
        fourmi.etape(grille)
        self.assertEqual(fourmi.direction, 1)  # Est
        self.assertEqual(fourmi.x, 2)
        self.assertEqual(fourmi.y, 1)
        self.assertEqual(grille.obtenir_couleur_case(1, 1), 1)  # La case devrait maintenant être noire

    def test_fourmi_limites(self):
        """Test que la fourmi ne sort pas des limites de la grille."""
        fourmi = Fourmi(0, 0, 0)
        grille = Grille(3, 3)
        fourmi.avancer(grille.largeur, grille.hauteur)
        self.assertEqual(fourmi.x, 0)
        self.assertEqual(fourmi.y, 0)  # Ne doit pas sortir de la grille

if __name__ == '__main__':
    unittest.main()
