import logging
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import timedelta
from my_fastapi_project.auth import authenticate_user, create_access_token, get_current_active_user, Token, User, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# In-memory storage
students = {}

# Pydantic models
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

    @validator('email')
    def email_must_be_unique(cls, v):
        if v in [student.email for student in students.values()]:
            raise ValueError('Email must be unique')
        return v

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
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
    Endpoint to return a HTML document with a name parameter.
    """
    return f"""
    <h1>Hello <span>{name}</span></h1>
    """

@app.post("/student", response_model=UUID)
def create_student(student: Student, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to create a new student.
    """
    students[student.id] = student
    return student.id

@app.get("/student/{student_id}", response_model=Student)
def read_student(student_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to get details of a student by ID.
    """
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/student/{student_id}")
def delete_student(student_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to delete a student by ID.
    """
    if student_id in students:
        del students[student_id]
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@app.get("/student/{student_id}/grades/{grade_id}", response_model=Grade)
def read_grade(student_id: UUID, grade_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to get a specific grade for a student.
    """
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for grade in student.grades:
        if grade.id == grade_id:
            return grade

    raise HTTPException(status_code=404, detail="Grade not found")

@app.delete("/student/{student_id}/grades/{grade_id}")
def delete_grade(student_id: UUID, grade_id: UUID, current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to delete a specific grade for a student.
    """
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for i, grade in enumerate(student.grades):
        if grade.id == grade_id:
            del student.grades[i]
            return {"message": "Grade deleted successfully"}

    raise HTTPException(status_code=404, detail="Grade not found")

@app.get("/export")
def export_data(format: Optional[str] = "csv", current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to export student data in JSON or CSV format.
    """
    # Functionality to export data in JSON or CSV format
    pass

# Global error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Une erreur inattendue est survenue : {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Une erreur inattendue est survenue."},
    )
