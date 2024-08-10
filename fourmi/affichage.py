"""
Module pour l'affichage de la grille de la Fourmi de Langton en utilisant Pygame.
"""

import pygame

def afficher_grille(fenetre, grille, taille_cellule, fourmis, marge=0):
    """Affiche la grille et les fourmis dans la fenêtre Pygame.

    Args:
        fenetre (pygame.Surface): La surface de la fenêtre Pygame.
        grille (Grille): La grille de la simulation.
        taille_cellule (int): La taille de chaque cellule en pixels.
        fourmis (list): La liste des fourmis à afficher.
        marge (int): La marge autour de la grille.
    """
    fenetre.fill((255, 255, 255))  # Fond blanc

    for y in range(grille.hauteur):
        for x in range(grille.largeur):
            couleur = (0, 0, 0) if grille.obtenir_couleur_case(x, y) == 1 else (255, 255, 255)
            rect = pygame.Rect(x * taille_cellule + marge, y * taille_cellule + marge, taille_cellule, taille_cellule)
            pygame.draw.rect(fenetre, couleur, rect)

    # Dessiner les fourmis
    for fourmi in fourmis:
        ant_rect = pygame.Rect(fourmi.x * taille_cellule + marge, fourmi.y * taille_cellule + marge, taille_cellule, taille_cellule)
        pygame.draw.rect(fenetre, (255, 0, 0), ant_rect)

    pygame.display.flip()
