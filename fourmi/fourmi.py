"""
Module représentant la Fourmi de Langton et ses comportements.
"""

class Fourmi:
    """Représente la fourmi de Langton.

    Attributs:
        DIRECTIONS (list): Les directions possibles que la fourmi peut prendre (N, E, S, O).
        x (int): La position actuelle en x de la fourmi.
        y (int): La position actuelle en y de la fourmi.
        direction (int): La direction actuelle de la fourmi (index dans DIRECTIONS).
        ant_id (int): L'identifiant unique de la fourmi.
    """

    DIRECTIONS = ['N', 'E', 'S', 'O']  # Nord, Est, Sud, Ouest

    def __init__(self, x, y, ant_id):
        """Initialise la fourmi à la position (x, y) et la direction initiale (Nord).

        Args:
            x (int): La position initiale en x.
            y (int): La position initiale en y.
            ant_id (int): L'identifiant unique de la fourmi.
        """
        self.x = x
        self.y = y
        self.direction = 0  # Commence en regardant vers le Nord
        self.ant_id = ant_id

    def tourner_a_droite(self):
        """Tourne la fourmi de 90 degrés vers la droite."""
        self.direction = (self.direction + 1) % 4

    def tourner_a_gauche(self):
        """Tourne la fourmi de 90 degrés vers la gauche."""
        self.direction = (self.direction - 1) % 4

    def avancer(self, largeur, hauteur):
        """Déplace la fourmi d'une case dans la direction actuelle, en tenant compte des limites de la grille.

        Args:
            largeur (int): La largeur de la grille.
            hauteur (int): La hauteur de la grille.
        """
        if self.DIRECTIONS[self.direction] == 'N':
            self.y -= 1
        elif self.DIRECTIONS[self.direction] == 'E':
            self.x += 1
        elif self.DIRECTIONS[self.direction] == 'S':
            self.y += 1
        elif self.DIRECTIONS[self.direction] == 'O':
            self.x -= 1

        # Assurer que la fourmi reste dans les limites de la grille
        self.x = max(0, min(self.x, largeur - 1))
        self.y = max(0, min(self.y, hauteur - 1))

    def etape(self, grille):
        """Exécute une étape de mouvement selon les règles de la fourmi de Langton.

        Args:
            grille (Grille): La grille sur laquelle la fourmi se déplace.
        """
        couleur_actuelle = grille.obtenir_couleur_case(self.x, self.y)
        if couleur_actuelle == 0:  # Case blanche
            self.tourner_a_droite()
        else:  # Case noire
            self.tourner_a_gauche()
        grille.changer_couleur_case(self.x, self.y)
        self.avancer(grille.largeur, grille.hauteur)
