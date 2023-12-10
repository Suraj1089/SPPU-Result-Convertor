from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from internal.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URI

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# instance of this class will be database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # base class to create database model
# all models will inherit from this base class


def get_db() -> None:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
