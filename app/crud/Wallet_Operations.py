#this file contains the crud operations for the wallet operations systemq
import db
from app.schema.Wallet_Operations import WalletOperationsSchema



def withdraw_money_from_wallet(user_id: int, amount: float, description: str):
    wallet = WalletOperations.query.filter_by(user_id=user_id).first()
    if wallet is None:
        return {"error": "Wallet not found"}, 404
    if wallet.balance < amount:
        return {"error": "Insufficient balance"}, 400
    wallet.balance -= amount
    db.session.commit()
    return WalletOperationsSchema.model_validate(wallet)


def add_money_to_wallet(user_id: int, amount: float, description: str):
    wallet = WalletOperations.query.filter_by(user_id=user_id).first()
    if wallet is None:
        return {"error": "Wallet not found"}, 404
    wallet.balance += amount
    db.session.commit()
    return WalletOperationsSchema.model_validate(wallet)


def get_wallet_balance(user_id: int):
    wallet = WalletOperations.query.filter_by(user_id=user_id).first()
    if wallet is None:
        return {"error": "Wallet not found"}, 404
    return WalletOperationsSchema.model_validate(wallet)
