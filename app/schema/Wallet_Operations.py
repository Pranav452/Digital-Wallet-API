#this file contains the schema for the wallet operations

from datetime import datetime
from pydantic import BaseModel

class WalletOperationsSchema(BaseModel):
    id: int
    user_id: int
    amount: float
    date: datetime