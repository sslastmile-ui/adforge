from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models import Base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./adforge.db")

if DATABASE_URL.startswith("postgres"):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
