#!/usr/bin/env python3
"""
Smart India Hackathon 2025 - Student Dropout Prediction System
Startup script to run the complete project
"""

import subprocess
import sys
import time
import os
import threading
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_ml_models():
    """Check if ML models exist"""
    models_path = Path("ml/models")
    required_models = ["decision_tree_model.pkl", "logistic_model.pkl", "scaler.pkl"]
    
    missing_models = []
    for model in required_models:
        if not (models_path / model).exists():
            missing_models.append(model)
    
    if missing_models:
        print(f"❌ Missing ML models: {missing_models}")
        print("🔧 Training models...")
        try:
            # Change to ml directory and run training
            original_dir = os.getcwd()
            os.chdir("ml")
            subprocess.check_call([sys.executable, "code/try1.py"])
            os.chdir(original_dir)
            print("✅ Models trained successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to train models: {e}")
            os.chdir(original_dir)
            return False
    else:
        print("✅ ML models found!")
        return True

def run_backend():
    """Run the Flask backend server"""
    print("🚀 Starting backend server...")
    try:
        subprocess.run([sys.executable, "backend/app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend server failed: {e}")
    except KeyboardInterrupt:
        print("🛑 Backend server stopped")

def run_frontend():
    """Run the Streamlit frontend"""
    print("🎨 Starting frontend dashboard...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed: {e}")
    except KeyboardInterrupt:
        print("🛑 Frontend stopped")

def main():
    print("=" * 60)
    print("🎓 SMART INDIA HACKATHON 2025")
    print("   Student Dropout Prediction System")
    print("=" * 60)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Setup failed. Please install requirements manually.")
        return
    
    # Step 2: Check/train ML models
    if not check_ml_models():
        print("❌ ML models not available. Please check the ml/ directory.")
        return
    
    print("\n🎯 Choose how to run the project:")
    print("1. Run both backend and frontend (recommended)")
    print("2. Run backend only (API server)")
    print("3. Run frontend only (dashboard)")
    print("4. Train ML models only")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting complete system...")
        print("📍 Backend will run on: http://localhost:5000")
        print("📍 Frontend will run on: http://localhost:8501")
        print("\n⚠️  Keep this terminal open. Press Ctrl+C to stop both servers.\n")
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Start frontend (this will block)
        try:
            run_frontend()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down system...")
    
    elif choice == "2":
        print("\n🚀 Starting backend server only...")
        print("📍 API will be available at: http://localhost:5000")
        print("📖 API documentation: http://localhost:5000")
        run_backend()
    
    elif choice == "3":
        print("\n🎨 Starting frontend dashboard only...")
        print("📍 Dashboard will be available at: http://localhost:8501")
        print("⚠️  Make sure backend is running on port 5000")
        run_frontend()
    
    elif choice == "4":
        print("\n🤖 Training ML models...")
        if check_ml_models():
            print("✅ ML models are ready!")
        else:
            print("❌ Model training failed")
    
    elif choice == "5":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Script interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the error and try again.")