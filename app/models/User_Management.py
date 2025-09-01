# this file contains the models for the user management system
from datetime import datetime
from db import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import DECIMAL

class UserManagement(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(index=True, unique=True, nullable=False, length=50)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False, length=100)
    password: Mapped[str] = mapped_column(nullable=False, length=255)
    phone_number: Mapped[str] = mapped_column(nullable=True, length=15)
    balance: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False, default=0.00)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relationship to transactions
    transactions = relationship("TransactionManagement", back_populates="user", foreign_keys="TransactionManagement.user_id")
    recipient_transactions = relationship("TransactionManagement", back_populates="recipient_user", foreign_keys="TransactionManagement.recipient_user_id")

    def __init__(self, username: str, email: str, password: str, phone_number: str = None):
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.balance = 0.00
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    