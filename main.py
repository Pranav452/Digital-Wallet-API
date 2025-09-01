#this file contains the main function for the application

from fastapi import FastAPI
from app.routers import User_Management, Wallet_Operations, Transaction_Management, Transfer_System
from db import Base, engine
import uvicorn

app = FastAPI()

app.include_router(User_Management.router)
app.include_router(Wallet_Operations.router)
app.include_router(Transaction_Management.router)
app.include_router(Transfer_System.router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)