import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if the environment is properly set up"""
    print("== Checking Environment Setup ==")
    
    # Check if SUT.pdf exists
    if os.path.exists("SUT.pdf"):
        print("✓ SUT.pdf found")
    else:
        print("✗ SUT.pdf not found - Please add the SUT.pdf file to the project directory")
    
    # Check if env variables are set
    if os.getenv("DATABASE_URL"):
        print("✓ DATABASE_URL environment variable is set")
    else:
        print("✗ DATABASE_URL environment variable is not set")
    
    # Check required directories
    required_dirs = [
        "app",
        "app/api",
        "app/db",
        "app/models",
        "app/schemas",
        "app/services",
        "app/static",
        "app/templates"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"✓ Directory {directory} exists")
        else:
            print(f"✗ Directory {directory} does not exist")
    
    # Check required files
    required_files = [
        "app/main.py",
        "app/api/prescription_routes.py",
        "app/db/database.py",
        "app/models/prescription.py",
        "app/schemas/prescription.py",
        "app/services/sut_service.py",
        "app/templates/index.html",
        "requirements.txt",
        ".env"
    ]
    
    for file in required_files:
        if os.path.exists(file) and os.path.isfile(file):
            print(f"✓ File {file} exists")
        else:
            print(f"✗ File {file} does not exist")
    
    print("\nEnvironment check completed.")

if __name__ == "__main__":
    check_environment()
    
    print("\nTo start the application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Initialize database: python init_db.py")
    print("3. Run the application: python run.py")
    print("4. Open in browser: http://localhost:8000") 