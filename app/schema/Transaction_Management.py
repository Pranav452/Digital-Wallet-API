# this file contains the schema for the transaction management system

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TransactionBase(BaseModel):
    user_id: int
    transaction_type: str
    amount: float = Field(gt=0, description="Transaction amount")
    description: Optional[str] = None

class TransactionCreateRequest(BaseModel):
    user_id: int
    transaction_type: str = Field(..., description="CREDIT, DEBIT, TRANSFER_IN, TRANSFER_OUT")
    amount: float = Field(gt=0, description="Transaction amount")
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    transaction_id: int
    transaction_type: str
    amount: float
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionDetailResponse(BaseModel):
    transaction_id: int
    user_id: int
    transaction_type: str
    amount: float
    description: Optional[str] = None
    recipient_user_id: Optional[int] = None
    reference_transaction_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    limit: int

    class Config:
        from_attributes = True

class TransactionManagementSchema(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    description: Optional[str] = None
    reference_transaction_id: Optional[int] = None
    recipient_user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True