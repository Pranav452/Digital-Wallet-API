#this file contains the schema for the transfer system

from datetime import datetime
from pydantic import BaseModel

class TransferSchema(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: float
    date: datetime