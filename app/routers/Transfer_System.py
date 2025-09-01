# this file contains the routers for the transfer system

from fastapi import APIRouter, Depends, HTTPException
from app.crud.Transfer_System import get_transfer, transfer_money
from app.schema.Transfer_System import (
    TransferRequest, TransferResponse, TransferDetailResponse
)
from sqlalchemy.orm import Session
from app.crud.Transfer_System import get_db

router = APIRouter(prefix="/transfer", tags=["Transfer System"])

@router.get("/{transfer_id}", response_model=TransferDetailResponse)
def get_transfer_endpoint(transfer_id: str, db: Session = Depends(get_db)):
    return get_transfer(transfer_id, db)

@router.post("", response_model=TransferResponse, status_code=201)
def transfer_money_endpoint(request: TransferRequest, db: Session = Depends(get_db)):
    return transfer_money(request, db)