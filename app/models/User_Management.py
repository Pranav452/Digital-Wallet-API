# this file contains the models for the user management system
from datetime import datetime

from db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class UserManagement(Base):
    __tablename__ = "user_management"

    id:Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username:Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    email:Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    password:Mapped[str] = mapped_column(index=True, nullable=False)
    phone_number:Mapped[str] = mapped_column(index=True, nullable=True)
    balance:Mapped[float] = mapped_column(index=True, nullable=False, default=0.0)
    created_at:Mapped[datetime] = mapped_column(index=True, nullable=False, default=datetime.now())
    updated_at:Mapped[datetime] = mapped_column(index=True, nullable=False, default=datetime.now())

    def __init__(self, username: str, email: str, password: str, phone_number: str):
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.balance = 0.0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    