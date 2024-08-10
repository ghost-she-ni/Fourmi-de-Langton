import httpx
import asyncio
import pygame
import json
import os
import logging
from fourmi.grille import Grille
from fourmi.fourmi import Fourmi
from fourmi.affichage import afficher_grille
from fourmi.config import lire_configuration

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sauvegarder l'état de la simulation
def sauvegarder_etat(state):
    """Sauvegarde l'état de la simulation dans un fichier JSON.

    Args:
        state (dict): L'état de la simulation à sauvegarder.
    """
    with open("sauvegarde.json", 'w', encoding='utf-8') as fichier:
        json.dump(state, fichier)
    logging.info("État de la simulation sauvegardé.")

# Reprendre l'état de la simulation
def reprendre_etat():
    """Reprend l'état de la simulation à partir d'un fichier JSON.

    Returns:
        dict: L'état de la simulation si le fichier existe, None sinon.
    """
    try:
        with open("sauvegarde.json", 'r', encoding='utf-8') as fichier:
            logging.info("État de la simulation repris depuis la sauvegarde.")
            return json.load(fichier)
    except FileNotFoundError:
        logging.warning("Aucune sauvegarde trouvée. Démarrage d'une nouvelle simulation.")
        return None

def nouvelle_partie(largeur, hauteur, nombre_de_fourmis):
    """Initialise une nouvelle partie avec une grille vide et les fourmis au centre.

    Args:
        largeur (int): La largeur de la grille.
        hauteur (int): La hauteur de la grille.
        nombre_de_fourmis (int): Le nombre de fourmis à initialiser.

    Returns:
        tuple: Une grille, une liste de fourmis, et l'état initial de la simulation.
    """
    grille = Grille(largeur, hauteur)
    fourmis = [Fourmi(largeur // 2, hauteur // 2, ant_id=i) for i in range(nombre_de_fourmis)]
    etat = {
        "grille": grille.grille,
        "fourmis": [{"x": f.x, "y": f.y, "direction": Fourmi.DIRECTIONS[f.direction], "id": f.ant_id} for f in fourmis]
    }
    logging.info("Nouvelle partie initialisée.")
    return grille, fourmis, etat

# Charger la clé secrète depuis les variables d'environnement
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La clé secrète n'est pas définie ! Assurez-vous qu'elle est dans les variables d'environnement.")

def afficher_menu(fenetre, police):
    """Affiche le menu de démarrage avec les options de l'utilisateur.

    Args:
        fenetre (pygame.Surface): La surface de la fenêtre Pygame.
        police (pygame.font.Font): La police utilisée pour afficher le texte.
    """
    fenetre.fill((255, 255, 255))  # Fond blanc
    titre = police.render("Simulation de la Fourmi de Langton", True, (0, 0, 0))
    option1 = police.render("1. Continuer la dernière partie", True, (0, 0, 0))
    option2 = police.render("2. Nouvelle partie", True, (0, 0, 0))
    instructions = police.render("Appuyez sur 1 ou 2 pour choisir une option", True, (0, 0, 0))

    fenetre.blit(titre, (50, 50))
    fenetre.blit(option1, (50, 150))
    fenetre.blit(option2, (50, 200))
    fenetre.blit(instructions, (50, 300))

    pygame.display.flip()

def menu_demarrage(fenetre):
    """Affiche le menu de démarrage et attend le choix de l'utilisateur.

    Args:
        fenetre (pygame.Surface): La surface de la fenêtre Pygame.

    Returns:
        str: Le choix de l'utilisateur ("continuer" ou "nouvelle").
    """
    police = pygame.font.SysFont('Arial', 24)
    afficher_menu(fenetre, police)

    en_attente = True
    choix = None

    while en_attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choix = 'continuer'
                    en_attente = False
                elif event.key == pygame.K_2:
                    choix = 'nouvelle'
                    en_attente = False

    logging.info(f"Choix de l'utilisateur: {choix}")
    return choix

async def envoyer_etat(client, etat):
    """Envoie l'état de la simulation au serveur de manière asynchrone.

    Args:
        client (httpx.AsyncClient): Le client HTTP asynchrone.
        etat (dict): L'état de la simulation à envoyer.
    """
    try:
        response = await client.post(
            "https://localhost:8000/update",
            json=etat,
            headers={"Authorization": f"Bearer {SECRET_KEY}"},
            verify=False  # Ignorer la vérification SSL pour le développement
        )
        if response.status_code != 200:
            logging.error(f"Erreur lors de l'envoi de l'état: {response.status_code}")
    except httpx.RequestError as e:
        logging.error(f"Erreur de connexion au serveur: {e}")

async def principal():
    """Point d'entrée principal pour la simulation avec Pygame."""
    config = lire_configuration()
    largeur, hauteur = config['largeur'], config['hauteur']
    taille_cellule = config['taille_cellule']
    etapes = config['etapes']
    nombre_de_fourmis = config.get('nombre_de_fourmis', 1)  # Par défaut, 1 fourmi

    # Initialiser Pygame
    pygame.init()
    fenetre = pygame.display.set_mode((largeur * taille_cellule, hauteur * taille_cellule))
    pygame.display.set_caption("Fourmi de Langton - Client")

    horloge = pygame.time.Clock()
    en_cours = True
    simulation_active = True

    # Afficher le menu de démarrage et obtenir le choix de l'utilisateur
    choix = menu_demarrage(fenetre)

    if choix == 'continuer':
        # Charger l'état initial ou reprendre la sauvegarde
        etat = reprendre_etat()
        if etat:
            logging.info("Reprise de la partie sauvegardée.")
            grille = Grille(largeur, hauteur)
            if len(etat["grille"]) == hauteur and all(len(ligne) == largeur for ligne in etat["grille"]):
                for y in range(hauteur):
                    for x in range(largeur):
                        grille.grille[y][x] = etat["grille"][y][x]
            else:
                logging.warning("Les dimensions de la grille sauvegardée ne correspondent pas aux dimensions spécifiées. Réinitialisation de la grille.")
                grille, fourmis, etat = nouvelle_partie(largeur, hauteur, nombre_de_fourmis)
            
            # Réinitialiser la liste de fourmis avant de charger celles de l'état sauvegardé
            fourmis = []
            for f in etat["fourmis"]:
                fourmi = Fourmi(f["x"], f["y"], f["id"])  # Utilisation de "id" pour l'initialisation
                fourmi.direction = Fourmi.DIRECTIONS.index(f["direction"])  # Convertir la direction texte en index
                fourmis.append(fourmi)
        else:
            logging.info("Aucune partie sauvegardée trouvée. Démarrage d'une nouvelle partie.")
            grille, fourmis, etat = nouvelle_partie(largeur, hauteur, nombre_de_fourmis)
    elif choix == 'nouvelle':
        logging.info("Démarrage d'une nouvelle partie.")
        grille, fourmis, etat = nouvelle_partie(largeur, hauteur, nombre_de_fourmis)

    vitesse_simulation = 10  # Vitesse de simulation initiale
    police = pygame.font.SysFont('Arial', 18)

    async with httpx.AsyncClient() as client:
        while en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_cours = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        simulation_active = not simulation_active  # Pause/reprise de la simulation
                        logging.info("Simulation mise en pause" if not simulation_active else "Simulation reprise")
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        vitesse_simulation += 1  # Augmenter la vitesse
                        logging.info(f"Vitesse de simulation augmentée à {vitesse_simulation}")
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        vitesse_simulation = max(1, vitesse_simulation - 1)  # Diminuer la vitesse
                        logging.info(f"Vitesse de simulation réduite à {vitesse_simulation}")
                    elif event.key == pygame.K_r:
                        # Reprendre la partie sauvegardée
                        logging.info("Reprise de la partie sauvegardée.")
                        etat = reprendre_etat()
                        if etat:
                            # Réinitialiser la grille et les fourmis
                            grille = Grille(largeur, hauteur)
                            fourmis = []
                            if len(etat["grille"]) == hauteur and all(len(ligne) == largeur for ligne in etat["grille"]):
                                for y in range(hauteur):
                                    for x in range(largeur):
                                        grille.grille[y][x] = etat["grille"][y][x]
                            else:
                                logging.warning("Les dimensions de la grille sauvegardée ne correspondent pas aux dimensions spécifiées. Réinitialisation de la grille.")
                                grille, fourmis, etat = nouvelle_partie(largeur, hauteur, nombre_de_fourmis)
                            
                            # Charger les fourmis de l'état sauvegardé
                            for f in etat["fourmis"]:
                                fourmi = Fourmi(f["x"], f["y"], f["id"])  # Utilisation de "id" pour l'initialisation
                                fourmi.direction = Fourmi.DIRECTIONS.index(f["direction"])  # Convertir la direction texte en index
                                fourmis.append(fourmi)
                    elif event.key == pygame.K_n:
                        # Nouvelle partie
                        logging.info("Démarrage d'une nouvelle partie.")
                        grille, fourmis, etat = nouvelle_partie(largeur, hauteur, nombre_de_fourmis)

            if simulation_active:
                for fourmi in fourmis:
                    fourmi.etape(grille)

                etat["fourmis"] = [{"x": f.x, "y": f.y, "direction": Fourmi.DIRECTIONS[f.direction], "id": f.ant_id} for f in fourmis]  # Changement de "id" en "ant_id"
                etat["grille"] = grille.grille

                afficher_grille(fenetre, grille, taille_cellule, fourmis)

                sauvegarder_etat(etat)

                # Envoi asynchrone de l'état au serveur
                asyncio.create_task(envoyer_etat(client, etat))

                texte_vitesse = police.render(f'Vitesse: {vitesse_simulation}', True, (0, 0, 0))
                fenetre.blit(texte_vitesse, (10, 10))

                if fourmis:
                    texte_info = police.render(f'Pos: ({fourmis[0].x}, {fourmis[0].y}) Dir: {Fourmi.DIRECTIONS[fourmis[0].direction]}', True, (0, 0, 0))
                    fenetre.blit(texte_info, (10, 50))

            horloge.tick(vitesse_simulation)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(principal())
