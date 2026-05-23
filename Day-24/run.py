#!/usr/bin/env python
"""Development server runner with automatic reload"""
import subprocess
import sys
import os

def main():
    """Run development server"""
    # Ensure environment is set
    if not os.path.exists(".env"):
        print("Error: .env file not found. Copy from .env.example")
        return 1
    
    # Run uvicorn
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
