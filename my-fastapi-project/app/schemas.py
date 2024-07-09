from pydantic import BaseModel, EmailStr
from typing import List

class MemberBase(BaseModel):
    name: str
    email: EmailStr
    category: str
    level: str
    age_group: str

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    name: str
    description: str
    category: str
    level: str
    age_group: str
    is_paid: bool
    fee: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    participants: List[Member] = []

    class Config:
        from_attributes = True
