"""
Module représentant la grille bidimensionnelle pour la simulation de la Fourmi de Langton.
"""

class Grille:
    """Représente une grille bidimensionnelle pour la simulation de la Fourmi de Langton.

    Attributs:
        largeur (int): La largeur de la grille.
        hauteur (int): La hauteur de la grille.
        grille (list): La représentation de la grille sous forme de liste de listes de zéros et de uns.
    """

    def __init__(self, largeur, hauteur):
        """Initialise la grille avec les dimensions spécifiées.

        Args:
            largeur (int): La largeur de la grille.
            hauteur (int): La hauteur de la grille.
        """
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[0 for _ in range(largeur)] for _ in range(hauteur)]
    
    def changer_couleur_case(self, x, y):
        """Inverse la couleur de la case (x, y).

        Args:
            x (int): La position en x de la case.
            y (int): La position en y de la case.
        """
        self.grille[y][x] = 1 - self.grille[y][x]

    def obtenir_couleur_case(self, x, y):
        """Retourne la couleur actuelle de la case (x, y).

        Args:
            x (int): La position en x de la case.
            y (int): La position en y de la case.

        Returns:
            int: La couleur de la case (0 pour blanc, 1 pour noir).
        """
        return self.grille[y][x]
