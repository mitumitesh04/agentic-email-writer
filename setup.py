# setup.py - Fixed for Windows
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    requirements = [
        "ollama-python",
        "streamlit"
    ]
    
    for package in requirements:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def setup_ollama():
    """Setup Ollama and pull model"""
    try:
        # Check if ollama is installed
        result = subprocess.run(["ollama", "--version"], capture_output=True)
        if result.returncode != 0:
            print("Ollama not found. Please install from https://ollama.com")
            return False
        
        # Pull the model
        print("Pulling phi3:mini model...")
        subprocess.run(["ollama", "pull", "phi3:3.8b-mini-4k-instruct-q4_0"])
        print("Model ready!")
        return True
        
    except FileNotFoundError:
        print("Ollama not found. Please install from https://ollama.com")
        return False

def create_run_script():
    """Create easy run script"""
    # Fixed: Use UTF-8 encoding and remove emojis for Windows compatibility
    script_content = """@echo off
echo Starting Email Generator Agent...
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
pause
"""
    
    # Fixed: Specify UTF-8 encoding
    with open("run.bat", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("Created run.bat file for Windows")

def main():
    print("Setting up Email Generator Agent...")
    
    # Install Python packages
    install_requirements()
    
    # Setup Ollama
    if setup_ollama():
        create_run_script()
        
        print("\nSetup complete!")
        print("\nTo run the app:")
        print("   streamlit run streamlit_app.py")
        print("\n   Or double-click: run.bat")
        print("\nThe app will open in your browser at http://localhost:8501")
    else:
        print("\nSetup incomplete. Please install Ollama first.")

if __name__ == "__main__":
    main()