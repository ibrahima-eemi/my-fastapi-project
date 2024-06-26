from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID, uuid4
from typing import List

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
