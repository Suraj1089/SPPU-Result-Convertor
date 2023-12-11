from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from internal.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URI

# engine = create_engine(SQLALCHEMY_DATABASE_URL)x

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=8, max_overflow=2,
                       pool_recycle=300, pool_pre_ping=True, pool_use_lifo=True)
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
