#this file contains the crud operations for the transfer systemPOST /transfer
from fastapi import HTTPException
from app.models.User_Management import UserManagement
from app.schema.Transfer_System import TransferSchema
import db



def get_transfer(transfer_id: int):
    transfer = TransferSchema.query.filter_by(id=transfer_id).first()
    if transfer is None:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return TransferSchema.model_validate(transfer)

def transfer_money(sender_user_id: int, recipient_user_id: int, amount: float, description: str):
    sender = UserManagement.query.filter_by(id=sender_user_id).first()
    recipient = UserManagement.query.filter_by(id=recipient_user_id).first()
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")
    if recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    sender.balance -= amount
    recipient.balance += amount
    db.session.commit()
    return TransferSchema.model_validate