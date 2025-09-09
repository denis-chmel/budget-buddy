from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from backend.services.auth import get_current_user
from backend.services.transactions import get_transaction_repo, TransactionRepository
from backend.models.user import User
from backend.schema.transactions import TransactionCreate, TransactionResponse

router = APIRouter(tags=["transactions"])

@router.post("/transactions")
def add_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_transaction_repo),
) -> TransactionResponse:
    """Create a new transaction for the authenticated user."""
    try:
        db_transaction = repo.create_transaction(transaction, current_user.id)
        return TransactionResponse(**db_transaction)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create transaction: {str(e)}"
        )

@router.get("/transactions")
def get_transactions(
    current_user: User = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_transaction_repo),
) -> List[TransactionResponse]:
    """Get all transactions for the authenticated user."""
    transactions = repo.get_user_transactions(current_user.id)
    return [TransactionResponse(**transaction) for transaction in transactions]

@router.delete("/transactions/{transaction_id}")
def remove_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    repo: TransactionRepository = Depends(get_transaction_repo),
):
    """Delete a transaction for the authenticated user."""
    success = repo.delete_transaction(transaction_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return {"message": "Transaction deleted successfully"}
