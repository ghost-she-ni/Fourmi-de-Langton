# Fourmi de Langton - Simulation Client/Serveur

## Description

Ce projet implémente la simulation de la Fourmi de Langton en utilisant une architecture client/serveur. Le serveur est développé avec FastAPI et le client utilise Pygame pour afficher la simulation.

## Prérequis

- Python 3.11
- Anaconda (optionnel mais recommandé)
- Pygame
- FastAPI
- Uvicorn
- PyYAML
- Requests
- Poetry (pour la gestion des dépendances)
- Certificat SSL (inclus dans le projet pour le développement)

## Installation

### 1. Cloner le dépôt

```bash
git clone <url_du_dépôt>
cd fourmi-de-langton
conda create --name environment python=3.11
conda activate environment

### 2.Utiliser Poetry pour installer les dépendances

Si vous n'avez pas Poetry installé, vous pouvez l'installer en suivant les instructions sur le site officiel de Poetry.
Ensuite, utilisez Poetry pour installer les dépendances :

```bash
poetry install

### 3.Activer l'environnement virtuel

Poetry crée un environnement virtuel pour le projet. Pour activer cet environnement :

```bash
poetry shell

### 4. Configuration des Variables d'Environnement

Définissez la clé secrète SECRET_KEY :

Windows :
```bash
set SECRET_KEY="votre_cle_secrete"

Unix/Linux/MacOS :
```bash
export SECRET_KEY="votre_cle_secrete"

## Utilisation
### 1. Lancer le Serveur
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --ssl-keyfile "./key.pem" --ssl-certfile "./cert.pem"

### 2. Lancer le Client
```bash
python client.py

##Tests
1. Exécuter les Tests Unitaires
```bash
pytest
