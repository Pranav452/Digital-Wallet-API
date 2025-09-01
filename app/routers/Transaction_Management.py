#this file contains the routers for the transaction management system

from fastapi import APIRouter
from app.crud.Transaction_Management import get_transactions
from app.crud.Transaction_Management import get_transaction_detail  
router = APIRouter()

router.get("/transactions/{user_id}")(get_transactions)
router.get("/transactions/detail/{transaction_id}")(get_transaction_detail)
router.post("/transactions")
