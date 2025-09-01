# this file contains the crud operations for the transfer system

from app.models.User_Management import UserManagement
from app.models.Transaction_Management import TransactionManagement
from app.schema.Transfer_System import (
    TransferRequest, TransferResponse, TransferDetailResponse, TransferErrorResponse
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

def get_transfer(transfer_id: str, db: Session = Depends(get_db)):
    # For simplicity, we'll use the reference_transaction_id to find transfers
    # In a real system, you might want a separate transfers table
    transaction = db.query(TransactionManagement).filter(
        TransactionManagement.reference_transaction_id == transfer_id
    ).first()
    
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transfer not found")
    
    # Find the corresponding sender transaction
    sender_transaction = db.query(TransactionManagement).filter(
        TransactionManagement.id == transaction.reference_transaction_id
    ).first()
    
    if sender_transaction is None:
        raise HTTPException(status_code=404, detail="Transfer not found")
    
    return TransferDetailResponse(
        transfer_id=transfer_id,
        sender_user_id=sender_transaction.user_id,
        recipient_user_id=transaction.user_id,
        amount=float(transaction.amount),
        description=transaction.description,
        status="completed",
        created_at=transaction.created_at
    )

def transfer_money(request: TransferRequest, db: Session = Depends(get_db)):
    # Validate sender and recipient
    sender = db.query(UserManagement).filter(UserManagement.id == request.sender_user_id).first()
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")
    
    recipient = db.query(UserManagement).filter(UserManagement.id == request.recipient_user_id).first()
    if recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # Check if sender and recipient are different
    if request.sender_user_id == request.recipient_user_id:
        raise HTTPException(status_code=400, detail="Sender and recipient cannot be the same")
    
    # Check sufficient balance
    if float(sender.balance) < request.amount:
        raise HTTPException(
            status_code=400, 
            detail="Insufficient balance",
            headers={"current_balance": str(sender.balance), "required_amount": str(request.amount)}
        )
    
    # Validate amount
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    try:
        # Generate unique transfer ID
        transfer_id = str(uuid.uuid4())
        
        # Create sender transaction (TRANSFER_OUT)
        sender_transaction = TransactionManagement(
            user_id=request.sender_user_id,
            transaction_type="TRANSFER_OUT",
            amount=request.amount,
            description=request.description or f"Transfer to user {request.recipient_user_id}",
            recipient_user_id=request.recipient_user_id
        )
        
        db.add(sender_transaction)
        db.flush()  # Get the ID without committing
        
        # Create recipient transaction (TRANSFER_IN)
        recipient_transaction = TransactionManagement(
            user_id=request.recipient_user_id,
            transaction_type="TRANSFER_IN",
            amount=request.amount,
            description=request.description or f"Transfer from user {request.sender_user_id}",
            reference_transaction_id=sender_transaction.id,
            recipient_user_id=request.sender_user_id
        )
        
        db.add(recipient_transaction)
        db.flush()  # Get the ID without committing
        
        # Link the transactions
        sender_transaction.reference_transaction_id = recipient_transaction.id
        
        # Update balances atomically
        sender.balance -= request.amount
        recipient.balance += request.amount
        sender.updated_at = datetime.now()
        recipient.updated_at = datetime.now()
        
        # Commit all changes
        db.commit()
        
        return TransferResponse(
            transfer_id=transfer_id,
            sender_transaction_id=sender_transaction.id,
            recipient_transaction_id=recipient_transaction.id,
            amount=request.amount,
            sender_new_balance=float(sender.balance),
            recipient_new_balance=float(recipient.balance),
            status="completed"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transfer failed: {str(e)}")