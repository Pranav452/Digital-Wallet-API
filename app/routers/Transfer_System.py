#this file contains the routers for the transfer system

from fastapi import APIRouter
from app.crud.Transfer_System import get_transfer, transfer_money


router = APIRouter()

router.get("/transfer/{transfer_id}")(get_transfer)
router.post("/transfer")(transfer_money)