#this file contains the routers for the wallet operations system

from fastapi import APIRouter
from app.crud.Wallet_Operations import get_wallet_balance, add_money_to_wallet, withdraw_money_from_wallet

router = APIRouter()

router.get("/wallet/{user_id}/balance")(get_wallet_balance)
router.post("/wallet/{user_id}/add-money")(add_money_to_wallet)
router.post("/wallet/{user_id}/withdraw")(withdraw_money_from_wallet)