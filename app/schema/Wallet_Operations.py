# this file contains the schema for the wallet operations system

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WalletBalanceRequest(BaseModel):
    pass

class WalletBalanceResponse(BaseModel):
    user_id: int
    balance: float
    last_updated: datetime

    class Config:
        from_attributes = True

class AddMoneyRequest(BaseModel):
    amount: float = Field(gt=0, description="Amount to add to wallet")
    description: Optional[str] = None

class AddMoneyResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str

    class Config:
        from_attributes = True

class WithdrawMoneyRequest(BaseModel):
    amount: float = Field(gt=0, description="Amount to withdraw from wallet")
    description: Optional[str] = None

class WithdrawMoneyResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str

    class Config:
        from_attributes = True

class WalletOperationsSchema(BaseModel):
    user_id: int
    balance: float

    class Config:
        from_attributes = True