from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional

class TransactionCreate(BaseModel):
    date: date
    amount: Decimal
    type: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    date: date
    amount: float
    type: Optional[str] = None

    class Config:
        from_attributes = True
