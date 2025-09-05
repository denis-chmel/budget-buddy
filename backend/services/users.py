from sqlalchemy.orm import Session
from backend.models.user import User
from backend.services.auth import hash_password

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, password: str) -> User:
    db_user = User(username=username, hashed_password=hash_password(password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()
