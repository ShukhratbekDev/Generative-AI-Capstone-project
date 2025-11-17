"""
Quick start script to initialize database and run the app.
"""
import subprocess
import sys
import os

def main():
    print("Initializing database...")
    from database import create_database
    create_database()
    print("Database initialized successfully!")
    print("\nStarting Streamlit app...")
    print("The app will open in your browser at http://localhost:8501")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()

