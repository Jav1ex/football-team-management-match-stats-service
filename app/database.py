"""
Database configuration module.

Sets up the SQLAlchemy engine and session for database interactions.
Dependencies: SQLAlchemy, databases.
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import databases

DATABASE_URL = "postgresql://postgres.olzrkkjzqltovkvxeggb:WbnS5utrc1Gayg35@aws-0-us-east-2.pooler.supabase.com:5432/postgres"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Databases instance for async operations
database = databases.Database(DATABASE_URL)

# Dependency for SQLAlchemy sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        