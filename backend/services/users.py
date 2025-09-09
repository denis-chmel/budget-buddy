from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, username: str, hashed_password: str) -> User:
        db_user = User(
            username=username,
            hashed_password=hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
