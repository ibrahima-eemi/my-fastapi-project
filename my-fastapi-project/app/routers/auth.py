from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials):
    correct_username = "ibrahima"
    correct_password = "diallo"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

@router.post("/token")
async def get_token(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    return {"token": "fake-jwt-token"}
