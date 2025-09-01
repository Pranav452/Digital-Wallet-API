# this file contains the routers for the user management system

from fastapi import APIRouter, Depends, HTTPException
from app.crud.User_Management import get_user, update_user, create_user
from app.schema.User_Management import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from sqlalchemy.orm import Session
from app.crud.User_Management import get_db

router = APIRouter(prefix="/users", tags=["User Management"])

@router.post("", response_model=UserResponseSchema, status_code=201)
def create_user_endpoint(user: UserCreateSchema, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id, db)

@router.put("/{user_id}", response_model=UserResponseSchema)
def update_user_endpoint(user_id: int, user_update: UserUpdateSchema, db: Session = Depends(get_db)):
    return update_user(user_id, user_update, db)