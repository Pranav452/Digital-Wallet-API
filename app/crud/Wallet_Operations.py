# this file contains the crud operations for the wallet operations system

from app.models.User_Management import UserManagement
from app.models.Transaction_Management import TransactionManagement
from app.schema.Wallet_Operations import (
    AddMoneyRequest, AddMoneyResponse, 
    WithdrawMoneyRequest, WithdrawMoneyResponse,
    WalletBalanceResponse
)
from db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from datetime import datetime
import uuid

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_wallet_balance(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserManagement).filter(UserManagement.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return WalletBalanceResponse(
        user_id=user.id,
        balance=float(user.balance),
        last_updated=user.updated_at
    )

def add_money_to_wallet(user_id: int, request: AddMoneyRequest, db: Session = Depends(get_db)):
    user = db.query(UserManagement).filter(UserManagement.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate amount
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Update user balance
    user.balance += request.amount
    user.updated_at = datetime.now()
    
    # Create transaction record
    transaction = TransactionManagement(
        user_id=user_id,
        transaction_type="CREDIT",
        amount=request.amount,
        description=request.description or "Added money to wallet"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(user)
    
    return AddMoneyResponse(
        transaction_id=transaction.id,
        user_id=user.id,
        amount=request.amount,
        new_balance=float(user.balance),
        transaction_type="CREDIT"
    )

def withdraw_money_from_wallet(user_id: int, request: WithdrawMoneyRequest, db: Session = Depends(get_db)):
    user = db.query(UserManagement).filter(UserManagement.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate amount
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Check sufficient balance
    if float(user.balance) < request.amount:
        raise HTTPException(
            status_code=400, 
            detail="Insufficient balance",
            headers={"current_balance": str(user.balance), "required_amount": str(request.amount)}
        )
    
    # Update user balance
    user.balance -= request.amount
    user.updated_at = datetime.now()
    
    # Create transaction record
    transaction = TransactionManagement(
        user_id=user_id,
        transaction_type="DEBIT",
        amount=request.amount,
        description=request.description or "Withdrew money from wallet"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(user)
    
    return WithdrawMoneyResponse(
        transaction_id=transaction.id,
        user_id=user.id,
        amount=request.amount,
        new_balance=float(user.balance),
        transaction_type="DEBIT"
    )
