# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite file-based DB in the project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Engine: low-level object that talks to the DB
# check_same_thread=False is required for SQLite + multi-threaded apps like uvicorn
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory: create Session objects for talking to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models (models will inherit from this)
Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()