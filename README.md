# My FastAPI Project

## Description

Ce projet utilise FastAPI pour créer une API REST avec des fonctionnalités d'authentification JWT, une gestion d'erreurs robuste et une gestion des étudiants et de leurs notes.

## Fonctionnalités

- Authentification via JWT
- CRUD pour les étudiants
- CRUD pour les notes des étudiants
- Exportation des données en format JSON ou CSV
- Gestion d'erreurs centralisée

## Prérequis

- Python 3.12+
- Poetry

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/ibrahima-eemi/my-fastapi-project.git
   cd my-fastapi-project
   ```

2. Installez les dépendances :
   ```bash
   poetry install
   ```

## Configuration

Assurez-vous que la structure de votre projet est comme suit :

```plaintext
my-fastapi-project/
├── my_fastapi_project/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
├── tests/
│   ├── __init__.py
├── generate_hash.py
├── pyproject.toml
├── README.md
├── start.sh
```

### Script `generate_hash.py`

Le script `generate_hash.py` est utilisé pour générer un hachage de mot de passe. Exécutez ce script pour générer le hachage du mot de passe que vous souhaitez utiliser dans la base de données fictive.

```python
from passlib.context import CryptContext

# Configuration de passlib pour utiliser bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mot de passe à hasher
password = "secret"

# Génération du hachage
hashed_password = pwd_context.hash(password)
print("Hashed password:", hashed_password)
```

Exécutez le script pour obtenir le hachage :
```bash
poetry run python generate_hash.py
```

### Mise à jour de `auth.py`

Assurez-vous que le fichier `auth.py` contient le hachage de mot de passe généré :
```python
hashed_password = "<hashed_password>"  # Remplacez <hashed_password> par le hachage généré
```

## Démarrage de l'application

Pour démarrer l'application, exécutez :

```bash
./start.sh
```

Cela lancera le serveur Uvicorn à `http://127.0.0.1:8000`.

## Utilisation

### Authentification

Pour obtenir un token JWT, utilisez l'endpoint `/token` avec les informations d'authentification appropriées.

Exemple avec cURL :
```bash
curl -X POST "http://127.0.0.1:8000/token" -d "username=johndoe&password=secret"
```

### Endpoints

- **POST** `/token`: Obtention d'un token JWT
  - Body : `username` et `password`

- **POST** `/student`: Création d'un nouvel étudiant (nécessite authentification)
  - Body : `first_name`, `last_name`, `email`, `grades`

- **GET** `/student/{student_id}`: Récupération des informations d'un étudiant par ID (nécessite authentification)

- **DELETE** `/student/{student_id}`: Suppression d'un étudiant par ID (nécessite authentification)

- **GET** `/student/{student_id}/grades/{grade_id}`: Récupération d'une note spécifique pour un étudiant (nécessite authentification)

- **DELETE** `/student/{student_id}/grades/{grade_id}`: Suppression d'une note spécifique pour un étudiant (nécessite authentification)

- **GET** `/export`: Exportation des données des étudiants en format JSON ou CSV (nécessite authentification)

### Exemple d'utilisation

#### Obtenir un token JWT

```bash
curl -X POST "http://127.0.0.1:8000/token" -d "username=johndoe&password=secret"
```

#### Créer un étudiant

```bash
curl -X POST "http://127.0.0.1:8000/student" -H "Authorization: Bearer <your-token>" -H "Content-Type: application/json" -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "johndoe@example.com",
  "grades": []
}'
```

#### Récupérer les informations d'un étudiant

```bash
curl -X GET "http://127.0.0.1:8000/student/<student-id>" -H "Authorization: Bearer <your-token>"
```

#### Supprimer un étudiant

```bash
curl -X DELETE "http://127.0.0.1:8000/student/<student-id>" -H "Authorization: Bearer <your-token>"
```

## Tests

Pour exécuter les tests, utilisez :

```bash
poetry run pytest
```

## Auteur

- Votre nom - [Votre Email](mailto:you@example.com)

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
```

Assurez-vous de remplacer `<url-du-repo>`, `<your-token>`, `<student-id>`, "Votre nom", et "Votre Email" par les informations appropriées.# my-fastapi-project
