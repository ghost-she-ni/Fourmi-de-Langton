from fastapi import FastAPI, HTTPException, Header
import hmac
import os
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "La clé secrète n'est pas définie ! Assurez-vous qu'elle est dans les variables d'environnement."
    )


def verify_token(token: str):
    """Vérifie que le jeton fourni est valide.

    Args:
        token (str): Le jeton d'authentification à vérifier.

    Raises:
        HTTPException: Si le jeton n'est pas valide.
    """
    if not hmac.compare_digest(token, SECRET_KEY):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token


@app.get("/state")
async def get_state(authorization: str = Header(None)):
    """Renvoie l'état actuel de la simulation.

    Args:
        authorization (str, optional): Le jeton d'autorisation. Defaults to Header(None).

    Returns:
        dict: L'état de la simulation contenant la grille et les fourmis.
    """
    token = authorization.split("Bearer ")[-1] if authorization else ""
    verify_token(token)
    state = {
        "grille": [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        "fourmis": [{"x": 1, "y": 1, "direction": "N"}],
    }
    logging.info("État de la simulation renvoyé.")
    return state


@app.post("/update")
async def update_state(state: dict, authorization: str = Header(None)):
    """Met à jour l'état de la simulation.

    Args:
        state (dict): L'état de la simulation à mettre à jour.
        authorization (str, optional): Le jeton d'autorisation. Defaults to Header(None).

    Returns:
        dict: L'état mis à jour de la simulation.
    """
    token = authorization.split("Bearer ")[-1] if authorization else ""
    verify_token(token)
    logging.info("État de la simulation mis à jour.")
    return state


if __name__ == "__main__":
    import uvicorn

    logging.info("Démarrage du serveur FastAPI avec SSL")
    uvicorn.run(
        app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem"
    )
