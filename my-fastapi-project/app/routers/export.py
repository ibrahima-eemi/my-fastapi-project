from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Member
import csv
import json
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials):
    if credentials.username != "ibrahima" or credentials.password != "diallo":
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/")
def export_data(format: str = "csv", db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    members = db.query(Member).all()
    if format == "csv":
        return StreamingResponse(generate_csv(members), media_type="text/csv")
    elif format == "json":
        return StreamingResponse(generate_json(members), media_type="application/json")
    else:
        raise HTTPException(status_code=400, detail="Invalid format")

def generate_csv(members):
    def iter_csv():
        header = ",".join([column.name for column in Member.__table__.columns])
        yield header + "\n"
        for member in members:
            row = ",".join([str(getattr(member, column.name)) for column in Member.__table__.columns])
            yield row + "\n"
    return iter_csv()

def generate_json(members):
    return json.dumps([member.__dict__ for member in members], default=str)
