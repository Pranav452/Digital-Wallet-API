# this file contains the models for the transaction management system

from sqlalchemy import ForeignKey, DECIMAL, String
from db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from sqlalchemy.orm import relationship

class TransactionManagement(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(10,2), index=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    reference_transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), index=True, nullable=True)
    recipient_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(index=True, nullable=False, default=datetime.now)
    
    # Relationships
    user = relationship("UserManagement", back_populates="transactions", foreign_keys=[user_id])
    recipient_user = relationship("UserManagement", back_populates="recipient_transactions", foreign_keys=[recipient_user_id])
    reference_transaction = relationship("TransactionManagement", remote_side=[id])
    
    def __init__(self, user_id: int, transaction_type: str, amount: float, description: str = None, 
                 reference_transaction_id: int = None, recipient_user_id: int = None):
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.reference_transaction_id = reference_transaction_id
        self.recipient_user_id = recipient_user_id
        self.created_at = datetime.now()
    