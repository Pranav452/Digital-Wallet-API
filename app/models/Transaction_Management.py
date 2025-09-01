# this file contains the models for the transaction management system

from sqlalchemy import ForeignKey
from db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from sqlalchemy.orm import relationship
class TransactionManagement(Base):
    __tablename__ = "transaction_management"
    
    id:Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user_management.id"), index=True, nullable=False)
    transaction_type:Mapped[str] = mapped_column( index=True, nullable=False)
    amount:Mapped[float] = mapped_column( index=True, nullable=False)
    description:Mapped[str] = mapped_column( index=True, nullable=True)
    reference_transaction_id:Mapped[int] = mapped_column(ForeignKey("transaction_management.id"), index=True, nullable=True)
    recipient_user_id:Mapped[int] = mapped_column(ForeignKey("user_management.id"), index=True, nullable=True)
    created_at:Mapped[datetime] = mapped_column(index=True, nullable=False, default=datetime.now())
    user = relationship("UserManagement", back_populates="transaction") 
    def __init__(self, user_id: int, transaction_type: str, amount: float, description: str, reference_transaction_id: int, recipient_user_id: int):
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.reference_transaction_id = reference_transaction_id
        self.recipient_user_id = recipient_user_id
        self.created_at = datetime.now()
    