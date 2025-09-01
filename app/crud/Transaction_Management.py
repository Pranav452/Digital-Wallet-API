# this file contains the crud operations for the transaction management system

from app.models.Transaction_Management import TransactionManagement
from app.schema.Transaction_Management import (
    TransactionCreateRequest, TransactionResponse, 
    TransactionDetailResponse, TransactionListResponse
)
from db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Query
from typing import List
from math import ceil

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_transactions(
    user_id: int, 
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Get total count
    total = db.query(TransactionManagement).filter(
        TransactionManagement.user_id == user_id
    ).count()
    
    # Get paginated transactions
    offset = (page - 1) * limit
    transactions = db.query(TransactionManagement).filter(
        TransactionManagement.user_id == user_id
    ).order_by(TransactionManagement.created_at.desc()).offset(offset).limit(limit).all()
    
    if not transactions:
        return TransactionListResponse(
            transactions=[],
            total=total,
            page=page,
            limit=limit
        )
    
    # Convert to response format
    transaction_responses = []
    for transaction in transactions:
        transaction_responses.append(TransactionResponse(
            transaction_id=transaction.id,
            transaction_type=transaction.transaction_type,
            amount=float(transaction.amount),
            description=transaction.description,
            created_at=transaction.created_at
        ))
    
    return TransactionListResponse(
        transactions=transaction_responses,
        total=total,
        page=page,
        limit=limit
    )

def get_transaction_detail(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(TransactionManagement).filter(
        TransactionManagement.id == transaction_id
    ).first()
    
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return TransactionDetailResponse(
        transaction_id=transaction.id,
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type,
        amount=float(transaction.amount),
        description=transaction.description,
        recipient_user_id=transaction.recipient_user_id,
        reference_transaction_id=transaction.reference_transaction_id,
        created_at=transaction.created_at
    )

def create_transaction(transaction: TransactionCreateRequest, db: Session = Depends(get_db)):
    # Validate transaction type
    valid_types = ["CREDIT", "DEBIT", "TRANSFER_IN", "TRANSFER_OUT"]
    if transaction.transaction_type not in valid_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid transaction type. Must be one of: {', '.join(valid_types)}"
        )
    
    # Validate amount
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Create transaction
    db_transaction = TransactionManagement(
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return TransactionDetailResponse(
        transaction_id=db_transaction.id,
        user_id=db_transaction.user_id,
        transaction_type=db_transaction.transaction_type,
        amount=float(db_transaction.amount),
        description=db_transaction.description,
        recipient_user_id=db_transaction.recipient_user_id,
        reference_transaction_id=db_transaction.reference_transaction_id,
        created_at=db_transaction.created_at
    )






