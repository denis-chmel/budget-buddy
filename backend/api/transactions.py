from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.services.auth import get_current_user
from backend.services.transactions import create_transaction, get_user_transactions, delete_transaction
from backend.models.user import User
from backend.schema.transactions import TransactionCreate, TransactionResponse

router = APIRouter(tags=["transactions"])

@router.post("/transactions")
def add_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new transaction for the authenticated user."""
    try:
        db_transaction = create_transaction(db, transaction, current_user.id)
        return db_transaction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create transaction: {str(e)}"
        )

@router.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[TransactionResponse]:
    """Get all transactions for the authenticated user."""
    transactions = get_user_transactions(db, current_user.id)
    return transactions

@router.delete("/transactions/{transaction_id}")
def remove_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a transaction for the authenticated user."""
    success = delete_transaction(db, transaction_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return {"message": "Transaction deleted successfully"}
