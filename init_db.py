import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath("."))

# Load environment variables
load_dotenv()

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    
    # Parse DATABASE_URL to extract connection info
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/danisman_eczacim")
    
    # Extract database name from URL
    db_name = db_url.split("/")[-1]
    
    # Create connection string without database name for initial connection
    conn_parts = db_url.split("/")
    conn_parts[-1] = "postgres"  # Connect to default postgres database
    conn_string = "/".join(conn_parts)
    
    # Connect to the default postgres database
    try:
        conn = psycopg2.connect(conn_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()
    
    # Initialize database tables
    from app.db.init_db import init_db
    init_db()
    
    print("Database initialization completed successfully.") 