from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(256), unique=True, nullable=True, index=True)
    full_name = Column(String(256), nullable=True)
    hashed_password = Column(String(256), nullable=False)

    # Relationship to Transaction
    transactions = relationship("Transaction", back_populates="user")
