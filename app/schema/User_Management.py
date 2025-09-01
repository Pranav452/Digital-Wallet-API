#this file contains the schema for the user management system

from datetime import datetime
from pydantic import BaseModel

class UserManagementSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str
    phone_number: str
    balance: float