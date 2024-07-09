# My FastAPI Project

## Description

Ce projet est une API de gestion d'une association sportive développée avec FastAPI. Elle permet de gérer les membres, les événements, l'authentification et l'exportation des données.

## Technologies Utilisées

- **Python 3.7**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **Uvicorn**
- **PostgreSQL**
- **dotenv**

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3.7**
- **Git**
- **PostgreSQL**

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/ibrahima-eemi/my-fastapi-project.git
    cd my-fastapi-project
    ```

2. Créez et activez un environnement virtuel :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Configurez les variables d'environnement :
    - Créez un fichier `.env` à la racine du projet.
    - Ajoutez la variable suivante à votre fichier `.env` :
        ```dotenv
        DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
        ```

## Utilisation

1. Démarrez le serveur Uvicorn :
    ```bash
    python -m uvicorn app.main:app --reload
    ```

2. Accédez à la documentation de l'API :
    - Swagger UI : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - ReDoc : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Points de terminaison de l'API

### Membres

- **POST /members/** : Créer un nouveau membre
- **GET /members/{member_id}** : Obtenir les détails d'un membre par ID
- **DELETE /members/{member_id}** : Supprimer un membre par ID

### Événements

- **GET /events/** : Lire les événements
- **POST /events/** : Créer un nouvel événement

### Authentification

- **POST /auth/token** : Obtenir un jeton JWT

### Exportation

- **GET /export** : Exporter les données des membres en JSON ou CSV

## Contribuer

1. Forkez le projet.
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`).
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`).
4. Poussez vers la branche (`git push origin feature/AmazingFeature`).
5. Ouvrez une Pull Request.

## Auteurs

- **[Ibrahima DIALLO](https://github.com/ibrahima-eemi)**

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
