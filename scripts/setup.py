#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return its output"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def setup_virtual_env():
    """Create and activate virtual environment"""
    print("Setting up Python virtual environment...")
    
    if platform.system() == "Windows":
        venv_activate = ".\\venv\\Scripts\\activate"
    else:
        venv_activate = "source venv/bin/activate"
    
    success, output = run_command("python -m venv venv")
    if not success:
        print("Failed to create virtual environment:", output)
        return False
    
    print("Virtual environment created successfully!")
    return True

def install_backend_deps():
    """Install backend dependencies"""
    print("Installing backend dependencies...")
    
    success, output = run_command("pip install -r requirements.txt")
    if not success:
        print("Failed to install backend dependencies:", output)
        return False
    
    print("Backend dependencies installed successfully!")
    return True

def install_frontend_deps():
    """Install frontend dependencies"""
    print("Installing frontend dependencies...")
    
    frontend_dir = Path("frontend")
    success, output = run_command("npm install", cwd=frontend_dir)
    if not success:
        print("Failed to install frontend dependencies:", output)
        return False
    
    print("Frontend dependencies installed successfully!")
    return True

def setup_database():
    """Initialize database and run migrations"""
    print("Setting up database...")
    
    success, output = run_command("python scripts/manage_db.py upgrade")
    if not success:
        print("Failed to setup database:", output)
        return False
    
    print("Database setup completed successfully!")
    return True

def create_env_files():
    """Create environment files from examples"""
    print("Creating environment files...")
    
    # Backend .env
    if not os.path.exists(".env") and os.path.exists(".env.example"):
        with open(".env.example", "r") as src, open(".env", "w") as dst:
            dst.write(src.read())
        print("Created backend .env file")
    
    # Frontend .env
    frontend_env = Path("frontend/.env")
    frontend_env_example = Path("frontend/.env.example")
    if not frontend_env.exists() and frontend_env_example.exists():
        with open(frontend_env_example, "r") as src, open(frontend_env, "w") as dst:
            dst.write(src.read())
        print("Created frontend .env file")

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "logs",
        "frontend/build",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def main():
    parser = argparse.ArgumentParser(description="Setup Student Tracking System")
    parser.add_argument("--skip-frontend", action="store_true", help="Skip frontend setup")
    parser.add_argument("--skip-venv", action="store_true", help="Skip virtual environment creation")
    args = parser.parse_args()

    # Create necessary directories
    create_directories()

    # Setup virtual environment
    if not args.skip_venv and not setup_virtual_env():
        sys.exit(1)

    # Create environment files
    create_env_files()

    # Install backend dependencies
    if not install_backend_deps():
        sys.exit(1)

    # Install frontend dependencies
    if not args.skip_frontend and not install_frontend_deps():
        sys.exit(1)

    # Setup database
    if not setup_database():
        sys.exit(1)

    print("\nSetup completed successfully!")
    print("\nTo start the application:")
    if platform.system() == "Windows":
        print("1. Backend: .\\venv\\Scripts\\activate && python src/api/routes.py")
    else:
        print("1. Backend: source venv/bin/activate && python src/api/routes.py")
    print("2. Frontend: cd frontend && npm start")

if __name__ == "__main__":
    main()
