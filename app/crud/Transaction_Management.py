#this file contains the crud operations for the transaction management system
from starlette.exceptions import HTTPException
from app.models.Transaction_Management import TransactionManagement
from app.schema.Transaction_Management import TransactionManagementSchema
import db


def get_transactions(user_id: int, page: int, limit: int):
    transactions = TransactionManagement.query.filter_by(user_id=user_id).paginate(page=page, per_page=limit)
    if transactions is None:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return TransactionManagementSchema.model_validate(transactions)

def get_transaction_detail(transaction_id: int):
    transaction = TransactionManagement.query.filter_by(id=transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionManagementSchema.model_validate(transaction)

def create_transaction(transaction: TransactionManagementSchema):
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction = TransactionManagement(**transaction.model_dump())
    db.session.add(transaction)
    db.session.commit()
    return TransactionManagementSchema.model_validate(transaction)






