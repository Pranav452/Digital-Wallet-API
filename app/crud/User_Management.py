#this file contains the crud operations for the user management system

from app.models.User_Management import UserManagement
from app.schema.User_Management import UserManagementSchema
import db
from sqlalchemy.orm import Session, query
from fastapi import HTTPException
def get_user(user_id: int):
    user = UserManagement.query.filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserManagementSchema.model_validate(user)


def update_user(user_id: int, user: UserManagementSchema):
    user = UserManagement.query.filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = user.username
    user.email = user.email
    user.password = user.password
    user.phone_number = user.phone_number
    db.session.commit()
    return UserManagementSchema.model_validate(user)

