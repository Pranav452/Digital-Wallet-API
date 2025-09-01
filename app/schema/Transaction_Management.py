#this file contains the schema for the transaction management system

from datetime import datetime
from pydantic import BaseModel

class TransactionManagementSchema(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    description: str
    reference_transaction_id: int
    recipient_user_id: int
    created_at: datetime