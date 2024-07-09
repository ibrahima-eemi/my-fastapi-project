import sys
import os

# Ajouter le répertoire parent au sys.path pour trouver le module app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Créer un moteur de base de données SQLite pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance de la base de données pour les tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Créer toutes les tables dans la base de données de test
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# Fonction pour réinitialiser la base de données
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Sports Association Management API"}

def test_create_member():
    reset_database()
    response = client.post(
        "/members/",
        json={"name": "John Doe", "email": "john@example.com", "category": "classique", "level": "intermédiaire", "age_group": "adolescent"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"

def test_create_event():
    reset_database()
    response = client.post(
        "/events/",
        json={"name": "Stage de Classique", "description": "Stage pour les adolescents", "category": "classique", "level": "intermédiaire", "age_group": "adolescent", "is_paid": True, "fee": 50}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Stage de Classique"
    assert response.json()["description"] == "Stage pour les adolescents"

def test_authentication():
    reset_database()
    response = client.post(
        "/auth/token",
        auth=("ibrahima", "diallo")
    )
    assert response.status_code == 200
    assert response.json() == {"token": "fake-jwt-token"}

def test_export_csv():
    reset_database()
    response = client.get("/export?format=csv", auth=("ibrahima", "diallo"))
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"

def test_export_json():
    reset_database()
    response = client.get("/export?format=json", auth=("ibrahima", "diallo"))
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

def test_authentication_fail():
    reset_database()
    response = client.get("/export?format=json", auth=("wrong", "credentials"))
    assert response.status_code == 401
