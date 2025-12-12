from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgresql", "postgresql+psycopg2")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
Generator function for managing the database session lifecycle.
Provides the session and closes it when finished using it.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
