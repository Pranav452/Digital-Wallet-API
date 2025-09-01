# this file contains the routers for the transaction management system

from fastapi import APIRouter, Depends, HTTPException, Query
from app.crud.Transaction_Management import get_transactions, create_transaction, get_transaction_detail
from app.schema.Transaction_Management import (
    TransactionCreateRequest, TransactionResponse, 
    TransactionDetailResponse, TransactionListResponse
)
from sqlalchemy.orm import Session
from app.crud.Transaction_Management import get_db

router = APIRouter(prefix="/transactions", tags=["Transaction Management"])

@router.get("/{user_id}", response_model=TransactionListResponse)
def get_transactions_endpoint(
    user_id: int, 
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_transactions(user_id, page, limit, db)

@router.get("/detail/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction_detail_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    return get_transaction_detail(transaction_id, db)

@router.post("", response_model=TransactionDetailResponse, status_code=201)
def create_transaction_endpoint(transaction: TransactionCreateRequest, db: Session = Depends(get_db)):
    return create_transaction(transaction, db)
