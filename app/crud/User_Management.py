# this file contains the crud operations for the user management system

from app.models.User_Management import UserManagement
from app.schema.User_Management import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from typing import Optional
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(UserManagement).filter(UserManagement.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = db.query(UserManagement).filter(UserManagement.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create new user
    db_user = UserManagement(
        username=user.username,
        email=user.email,
        password=user.password,  # In production, hash this password
        phone_number=user.phone_number
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponseSchema(
        user_id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        phone_number=db_user.phone_number,
        balance=float(db_user.balance),
        created_at=db_user.created_at
    )

def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserManagement).filter(UserManagement.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponseSchema(
        user_id=user.id,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        balance=float(user.balance),
        created_at=user.created_at
    )

def update_user(user_id: int, user_update: UserUpdateSchema, db: Session = Depends(get_db)):
    db_user = db.query(UserManagement).filter(UserManagement.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    if user_update.username is not None:
        # Check if new username already exists
        if user_update.username != db_user.username:
            existing_user = db.query(UserManagement).filter(UserManagement.username == user_update.username).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Username already exists")
        db_user.username = user_update.username
    
    if user_update.phone_number is not None:
        db_user.phone_number = user_update.phone_number
    
    db_user.updated_at = datetime.now()
    db.commit()
    db.refresh(db_user)
    
    return UserResponseSchema(
        user_id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        phone_number=db_user.phone_number,
        balance=float(db_user.balance),
        created_at=db_user.created_at
    )

