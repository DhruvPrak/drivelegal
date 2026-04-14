# app/db/database.py
# This file handles the database connection
# Every time FastAPI needs to talk to PostgreSQL, it uses this

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Get database URL from .env file
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://drivelegal:drivelegal123@localhost:5432/drivelegal"
)

# Create the database engine
# This is the actual connection to PostgreSQL
# pool_pre_ping=True — tests connection before using it
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal — a factory that creates database sessions
# Each request gets its own session
# autocommit=False — we manually commit changes
# autoflush=False — we manually flush changes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base — all our database models will inherit from this
# It keeps track of all tables we define
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI
    Creates a database session for each request
    Automatically closes it when request is done
    
    Usage in routes:
    def my_route(db: Session = Depends(get_db)):
        ...
    """
    db = SessionLocal()
    try:
        yield db          # give the session to the route
    finally:
        db.close()        # always close, even if error occurs