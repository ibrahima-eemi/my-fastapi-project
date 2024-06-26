from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import timedelta
from my_fastapi_project.auth import authenticate_user, create_access_token, get_current_active_user, Token, User, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

# Modèles Pydantic
class Grade(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    course: str
    score: float = Field(..., ge=0, le=100)

class Student(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr
    grades: List[Grade] = []

# Stockage en mémoire
students = {}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint pour authentifier un utilisateur et retourner un token JWT.
    
    Args:
    form_data (OAuth2PasswordRequestForm): Contient le nom d'utilisateur et le mot de passe.

    Returns:
    dict: Token d'accès et type de token.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", response_class=HTMLResponse)
def read_root(name: Optional[str] = "World"):
    """
    Endpoint pour retourner un document HTML avec un paramètre de nom.
    
    Args:
    name (str, optional): Le nom à inclure dans la réponse HTML. Par défaut "World".

    Returns:
    str: Contenu HTML.
    """
    return f"""
    <h1>Hello <span>{name}</span></h1>
    """

@app.post("/student", response_model=UUID)
def create_student(student: Student, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint pour créer un nouvel étudiant.
    
    Args:
    student (Student): Les données de l'étudiant.
    current_user (User, optional): L'utilisateur authentifié.

    Returns:
    UUID: L'ID de l'étudiant créé.
    """
    students[student.id] = student
    return student.id

@app.get("/student/{student_id}", response_model=Student)
def read_student(student_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint pour obtenir les détails d'un étudiant par ID.
    
    Args:
    student_id (UUID): L'ID de l'étudiant.
    current_user (User, optional): L'utilisateur authentifié.

    Returns:
    Student: Les détails de l'étudiant.
    """
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return student

@app.delete("/student/{student_id}")
def delete_student(student_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint pour supprimer un étudiant par ID.
    
    Args:
    student_id (UUID): L'ID de l'étudiant.
    current_user (User, optional): L'utilisateur authentifié.

    Returns:
    dict: Message de succès.
    """
    if student_id in students:
        del students[student_id]
        return {"message": "Étudiant supprimé avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

@app.get("/student/{student_id}/grades/{grade_id}", response_model=Grade)
def read_grade(student_id: UUID, grade_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint pour obtenir une note spécifique d'un étudiant.
    
    Args:
    student_id (UUID): L'ID de l'étudiant.
    grade_id (UUID): L'ID de la note.
    current_user (User, optional): L'utilisateur authentifié.

    Returns:
    Grade: Les détails de la note.
    """
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    for grade in student.grades:
        if grade.id == grade_id:
            return grade

    raise HTTPException(status_code=404, detail="Note non trouvée")

@app.delete("/student/{student_id}/grades/{grade_id}")
def delete_grade(student_id: UUID, grade_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint pour supprimer une note spécifique d'un étudiant.
    
    Args:
    student_id (UUID): L'ID de l'étudiant.
    grade_id (UUID): L'ID de la note.
    current_user (User, optional): L'utilisateur authentifié.

    Returns:
    dict: Message de succès.
    """
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    for i, grade in enumerate(student.grades):
        if grade.id == grade_id:
            del student.grades[i]
            return {"message": "Note supprimée avec succès"}

    raise HTTPException(status_code=404, detail="Note non trouvée")

@app.get("/export")
def export_data(format: Optional[str] = "csv", current_user: User = Depends(get_current_active_user)):
    """
    Endpoint pour exporter les données des étudiants en format JSON ou CSV.
    
    Args:
    format (str, optional): Le format d'exportation, soit "json" soit "csv". Par défaut "csv".

    Returns:
    Réponse JSON ou CSV avec les données des étudiants.
    """
    # Fonctionnalité pour exporter les données en format JSON ou CSV
    pass

# Gestion globale des erreurs
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Gestionnaire d'exceptions HTTP pour retourner une réponse JSON.
    
    Args:
    request: La requête.
    exc (HTTPException): L'exception HTTP.

    Returns:
    JSONResponse: Réponse JSON avec le code de statut et le message de l'erreur.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Gestionnaire global des exceptions pour retourner une réponse JSON.
    
    Args:
    request: La requête.
    exc (Exception): L'exception.

    Returns:
    JSONResponse: Réponse JSON avec un code de statut 500 et un message d'erreur général.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Une erreur inattendue est survenue."},
    )
