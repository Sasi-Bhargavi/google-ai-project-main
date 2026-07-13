# run_local.py
import os
import sys
import subprocess
import shutil

def verify_and_deploy():
    print("🚀 [EduGenie Deployment Engine] Initializing environment checks...")

    # 1. Check Python Version (Requires 3.10+)
    if sys.version_info < (3, 10):
        sys.exit("❌ Error: EduGenie requires Python 3.10 or higher due to type hint dependencies.")

    # 2. Check for .env file configuration
    if not os.path.exists(".env"):
        print("⚠️ Warning: .env file not found. Creating a baseline configuration template...")
        with open(".env", "w") as f:
            f.write('GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"\nENVIRONMENT="development"\n')
        print("❌ Critical: Please update the newly generated '.env' file with your active Gemini API Key.")
        sys.exit(1)

    # 3. Verify directory architecture integrity
    required_dirs = ["static/css", "templates", "core"]
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"📁 Structuring missing runtime asset directory layout: {directory}")
            os.makedirs(directory, exist_ok=True)

    # 4. Auto-install or upgrade dependencies
    print("📦 Synchronizing project execution dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        sys.exit("❌ Error: Dependency resolution failed during pip synchronization.")

    # 5. Boot local production server cluster via Uvicorn
    print("\n⚡ Booting EduGenie Local App Engine Hub via Uvicorn...")
    print("🔗 Point your browser instance directly to: http://127.0.0.1:8000\n")
    
    try:
        # Runs uvicorn directly within the active terminal process loop
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\n🛑 [EduGenie Deployment Engine] Local server instance cluster successfully terminated by user request.")

if __name__ == "__main__":
    verify_and_deploy()