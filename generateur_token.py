import secrets

cle_secrete = secrets.token_hex(
    32
)  # Génère une clé secrète de 64 caractères hexadécimaux
print(cle_secrete)
