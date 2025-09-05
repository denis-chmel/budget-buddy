from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from backend.core.settings import settings
from typing import Generator

Base = declarative_base()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 10}
)

SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
