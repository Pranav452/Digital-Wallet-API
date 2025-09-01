# this file contains the main function for the application

from fastapi import FastAPI, HTTPException
from app.routers import User_Management, Wallet_Operations, Transaction_Management, Transfer_System
from db import Base, engine, SessionLocal
from app.models.User_Management import UserManagement
from app.models.Transaction_Management import TransactionManagement
from app.schema.User_Management import UserCreateSchema
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI(
    title="Digital Wallet API",
    description="A FastAPI backend for a digital wallet system",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Digital Wallet API",
        "description": "Manage your wallet, transactions and transfers",
        "documentation": "/docs",
        "endpoints": {
            "users": "/users",
            "wallet": "/wallet",
            "transactions": "/transactions",
            "transfer": "/transfer"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Digital Wallet API is running"}

# Include routers
app.include_router(User_Management.router)
app.include_router(Wallet_Operations.router)
app.include_router(Transaction_Management.router)
app.include_router(Transfer_System.router)

# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)