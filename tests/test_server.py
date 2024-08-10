"""
Tests unitaires pour le serveur FastAPI de la simulation de la Fourmi de Langton.
"""

import sys
import os
from fastapi.testclient import TestClient

# Ajouter le chemin du projet pour permettre l'importation correcte des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Les importations des modules du projet doivent venir après la configuration du chemin
from server import app, SECRET_KEY

client = TestClient(app)

def test_get_state():
    """Test pour la route GET /state."""
    response = client.get("/state", headers={"Authorization": f"Bearer {SECRET_KEY}"})
    assert response.status_code == 200
    data = response.json()
    assert "grille" in data
    assert "fourmis" in data  # Vérifier que "fourmis" est présent
    assert isinstance(data["fourmis"], list)  # Vérifier que "fourmis" est une liste
    assert len(data["fourmis"]) > 0  # Vérifier qu'il y a au moins une fourmi dans la liste

def test_update_state():
    """Test pour la route POST /update."""
    new_state = {
        "grille": [
            [1, 1, 1],
            [0, 0, 0],
            [1, 1, 1]
        ],
        "fourmis": [
            {"x": 2, "y": 2, "direction": "E", "id": 0}
        ]
    }
    response = client.post("/update", json=new_state, headers={"Authorization": f"Bearer {SECRET_KEY}"})
    assert response.status_code == 200
    data = response.json()
    assert data == new_state
