from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Import models
from app.models.prescription import Prescription
from app.db.database import Base, engine

# Create all tables in the database
def init_db():
    # Drop all tables first to ensure clean state (only for development)
    # Base.metadata.drop_all(bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db() 