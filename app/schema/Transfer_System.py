# this file contains the schema for the transfer system

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransferRequest(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float = Field(gt=0, description="Transfer amount")
    description: Optional[str] = None

class TransferResponse(BaseModel):
    transfer_id: str
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float
    sender_new_balance: float
    recipient_new_balance: float
    status: str

    class Config:
        from_attributes = True

class TransferDetailResponse(BaseModel):
    transfer_id: str
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class TransferErrorResponse(BaseModel):
    error: str
    current_balance: float
    required_amount: float

class TransferSchema(BaseModel):
    id: int
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True