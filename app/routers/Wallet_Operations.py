# this file contains the routers for the wallet operations system

from fastapi import APIRouter, Depends, HTTPException
from app.crud.Wallet_Operations import get_wallet_balance, add_money_to_wallet, withdraw_money_from_wallet
from app.schema.Wallet_Operations import (
    AddMoneyRequest, AddMoneyResponse, 
    WithdrawMoneyRequest, WithdrawMoneyResponse,
    WalletBalanceResponse
)
from sqlalchemy.orm import Session
from app.crud.Wallet_Operations import get_db

router = APIRouter(prefix="/wallet", tags=["Wallet Operations"])

@router.get("/{user_id}/balance", response_model=WalletBalanceResponse)
def get_wallet_balance_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_wallet_balance(user_id, db)

@router.post("/{user_id}/add-money", response_model=AddMoneyResponse, status_code=201)
def add_money_to_wallet_endpoint(user_id: int, request: AddMoneyRequest, db: Session = Depends(get_db)):
    return add_money_to_wallet(user_id, request, db)

@router.post("/{user_id}/withdraw", response_model=WithdrawMoneyResponse, status_code=201)
def withdraw_money_from_wallet_endpoint(user_id: int, request: WithdrawMoneyRequest, db: Session = Depends(get_db)):
    return withdraw_money_from_wallet(user_id, request, db)