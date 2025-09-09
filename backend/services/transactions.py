from fastapi import Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.transaction import Transaction
from backend.schema.transactions import TransactionCreate


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(
        self, transaction_data: TransactionCreate,
       user_id: int,
    ) -> dict:
        """Create a new transaction for a user"""
        db_transaction = Transaction(
            user_id=user_id,
            date=transaction_data.date,
            amount=transaction_data.amount,
            type=transaction_data.type
        )
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)

        return {
            "id": str(db_transaction.id),
            "date": db_transaction.date.isoformat(),
            "amount": float(db_transaction.amount),
            "type": db_transaction.type,
        }

    def get_user_transactions(self, user_id: int) -> list[dict]:
        transactions = (
            self.db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(
                Transaction.date.desc(),
                Transaction.id.desc()
            )
            .all()
        )
        return [
            {
                "id": str(transaction.id),
                "date": transaction.date.isoformat(),
                "amount": float(transaction.amount),
                "type": transaction.type,
            }
            for transaction in transactions
        ]

    def get_transaction_by_id(self, transaction_id: int, user_id: int) -> Transaction:
        """Get a specific transaction by ID, ensuring it belongs to the user"""
        return self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()

    def delete_transaction(self, transaction_id: int, user_id: int) -> bool:
        """Delete a transaction, ensuring it belongs to the user"""
        transaction = self.get_transaction_by_id(transaction_id, user_id)
        if transaction:
            self.db.delete(transaction)
            self.db.commit()
            return True
        return False

def get_transaction_repo(db: Session = Depends(get_db)) -> TransactionRepository:
    return TransactionRepository(db)
