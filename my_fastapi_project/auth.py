from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Clé secrète pour JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Utiliser le hachage généré
hashed_password = "$2b$12$Q9dhJTPb9pDSeFWe83Kpc.nQFSATYvEJ5RF.Q19P8AambIf6cVKZ6"  # Remplacez <hashed_password> par le hachage généré

# Base de données fictive des utilisateurs
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": hashed_password,
        "disabled": False,
    }
}

# Configuration de Passlib pour utiliser bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modèles Pydantic
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    """
    Vérifie si le mot de passe en clair correspond au mot de passe haché.
    
    Args:
    plain_password (str): Le mot de passe en clair.
    hashed_password (str): Le mot de passe haché.

    Returns:
    bool: True si le mot de passe correspond, False sinon.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Génère le hachage d'un mot de passe.
    
    Args:
    password (str): Le mot de passe en clair.

    Returns:
    str: Le mot de passe haché.
    """
    return pwd_context.hash(password)

def get_user(db, username: str):
    """
    Récupère un utilisateur de la base de données fictive.
    
    Args:
    db (dict): La base de données fictive.
    username (str): Le nom d'utilisateur.

    Returns:
    UserInDB: Les informations de l'utilisateur.
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    """
    Authentifie un utilisateur en vérifiant son nom d'utilisateur et son mot de passe.
    
    Args:
    fake_db (dict): La base de données fictive.
    username (str): Le nom d'utilisateur.
    password (str): Le mot de passe en clair.

    Returns:
    UserInDB: Les informations de l'utilisateur si authentifié, False sinon.
    """
    try:
        user = get_user(fake_db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    except Exception as e:
        logger.error(f"Erreur lors de l'authentification de l'utilisateur {username}: {e}")
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crée un token JWT pour l'utilisateur authentifié.
    
    Args:
    data (dict): Les données à inclure dans le token.
    expires_delta (Optional[timedelta]): La durée de validité du token.

    Returns:
    str: Le token JWT encodé.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Récupère l'utilisateur actuel à partir du token JWT.
    
    Args:
    token (str): Le token JWT.

    Returns:
    User: Les informations de l'utilisateur.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Vérifie si l'utilisateur actuel est actif.
    
    Args:
    current_user (User): Les informations de l'utilisateur actuel.

    Returns:
    User: Les informations de l'utilisateur s'il est actif.

    Raises:
    HTTPException: Si l'utilisateur est inactif.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Utilisateur inactif")
    return current_user
