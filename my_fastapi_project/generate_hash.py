from passlib.context import CryptContext

# Configuration de passlib pour utiliser bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mot de passe à hasher
password = "secret"

# Génération du hachage
hashed_password = pwd_context.hash(password)
print("Hashed password:", hashed_password)
