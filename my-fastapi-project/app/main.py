from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routers import members, events, auth, export
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(members.router, prefix="/members", tags=["members"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(auth.router)
app.include_router(export.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Sports Association Management API",
        "documentation_url": "/docs"
    }

@app.get("/test-db-connection")
def test_db_connection():
    try:
        with engine.connect() as connection:
            return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}
