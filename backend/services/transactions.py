from sqlalchemy.orm import Session
from backend.models.transaction import Transaction
from backend.schema.transactions import TransactionCreate
from datetime import date
from decimal import Decimal

def create_transaction(db: Session, transaction_data: TransactionCreate, user_id: int) -> dict:
    """Create a new transaction for a user"""
    db_transaction = Transaction(
        user_id=user_id,
        date=transaction_data.date,
        amount=transaction_data.amount,
        type=transaction_data.type
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return {
        "id": str(db_transaction.id),
        "date": db_transaction.date.isoformat(),
        "amount": float(db_transaction.amount),
        "type": db_transaction.type,
    }

def get_user_transactions(db: Session, user_id: int) -> list[dict]:
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.date.desc(), Transaction.id.desc()).all()
    return [
        {
            "id": str(transaction.id),
            "date": transaction.date.isoformat(),
            "amount": float(transaction.amount),
            "type": transaction.type,
        }
        for transaction in transactions
    ]

def get_transaction_by_id(db: Session, transaction_id: int, user_id: int) -> Transaction:
    """Get a specific transaction by ID, ensuring it belongs to the user"""
    return db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id
    ).first()

def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    """Delete a transaction, ensuring it belongs to the user"""
    transaction = get_transaction_by_id(db, transaction_id, user_id)
    if transaction:
        db.delete(transaction)
        db.commit()
        return True
    return False
