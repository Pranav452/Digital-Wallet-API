#this file contains the crud operations for the wallet operations systemq
import db
from app.schema.Wallet_Operations import WalletOperationsSchema
from fastapi import HTTPException



def withdraw_money_from_wallet(user_id: int, amount: float, description: str):
    wallet = WalletOperations.query.filter_by(user_id=user_id).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    wallet.balance -= amount
    db.session.commit()
    return WalletOperationsSchema.model_validate(wallet)


def add_money_to_wallet(user_id: int, amount: float, description: str):
    wallet = WalletOperations.query.filter_by(user_id=user_id).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet.balance += amount
    db.session.commit()
    return WalletOperationsSchema.model_validate(wallet)


def get_wallet_balance(user_id: int):
    wallet = WalletOperations.query.filter_by(user_id=user_id).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletOperationsSchema.model_validate(wallet)
