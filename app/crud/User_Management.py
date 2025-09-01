#this file contains the crud operations for the user management system

from app.models.User_Management import UserManagement
from app.schema.User_Management import UserManagementSchema
import db

def create_user(user: UserManagementSchema):
    user = UserManagement(username=user.username, email=user.email, password=user.password, phone_number=user.phone_number)
    db.session.add(user)
    db.session.commit()
    return UserManagementSchema.model_validate(user)

def get_user(user_id: int):
    user = UserManagement.query.filter_by(id=user_id).first()
    return UserManagementSchema.model_validate(user)


def update_user(user_id: int, user: UserManagementSchema):
    user = UserManagement.query.filter_by(id=user_id).first()
    user.username = user.username
    user.phone_number = user.phone_number
    db.session.commit()
    return UserManagementSchema.model_validate(user)

