# this file contains the schema for the user management system

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: Optional[str] = None

class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponseSchema(BaseModel):
    user_id: int
    username: str
    email: str
    phone_number: Optional[str] = None
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True

class UserManagementSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str
    phone_number: Optional[str] = None
    balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True