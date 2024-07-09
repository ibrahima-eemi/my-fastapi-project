from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    category = Column(String)
    level = Column(String)
    age_group = Column(String)
    is_active = Column(Boolean, default=True)

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String)
    level = Column(String)
    age_group = Column(String)
    is_paid = Column(Boolean, default=False)
    fee = Column(Integer, default=0)
    participants = relationship("Member", secondary="event_participants")

class EventParticipant(Base):
    __tablename__ = "event_participants"
    
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), primary_key=True)
