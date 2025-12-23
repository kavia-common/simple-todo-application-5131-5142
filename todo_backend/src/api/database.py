from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base

import os

# Use environment variable for DB path or default to local file
DATABASE_URL = os.getenv("SQLITE_DB", "sqlite:///./todos.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# PUBLIC_INTERFACE
def create_db_and_tables():
    """Create the todos table if it does not exist."""
    Base.metadata.create_all(bind=engine)
