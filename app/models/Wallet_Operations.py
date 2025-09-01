# this file contains the models for the wallet operations

from db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from pydantic import BaseModel

class WalletOperations(Base):
    __tablename__ = "wallet_operations"
    id:Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user_management.id"), index=True, nullable=False)
    amount:Mapped[float] = mapped_column( index=True, nullable=False)   
    date:Mapped[datetime] = mapped_column( index=True, nullable=False)

class WalletOperationsSchema(BaseModel):
    id: int
    user_id: int
    amount: float
    date: datetime