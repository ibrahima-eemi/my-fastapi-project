from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    new_event = models.Event(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events