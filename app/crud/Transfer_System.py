#this file contains the crud operations for the transfer systemPOST /transfer
from app.models.User_Management import UserManagement
from app.schema.Transfer_System import TransferSchema
import db



def get_transfer(transfer_id: int):
    transfer = TransferSchema.query.filter_by(id=transfer_id).first()
    return TransferSchema.model_validate(transfer)

def transfer_money(sender_user_id: int, recipient_user_id: int, amount: float, description: str):
    sender = UserManagement.query.filter_by(id=sender_user_id).first()
    recipient = UserManagement.query.filter_by(id=recipient_user_id).first()
    if sender.balance < amount:
        return {"error": "Insufficient balance"}, 400
    sender.balance -= amount
    recipient.balance += amount
    db.session.commit()
    return TransferSchema.model_validate