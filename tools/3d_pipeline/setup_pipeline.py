#!/usr/bin/env python3
"""
Simple pipeline setup script without Unicode issues
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_pipeline():
    """Setup the 3D pipeline"""
    print("Setting up Hades-Quality 3D Pipeline...")
    
    # Install dependencies
    requirements_path = Path(__file__).parent / "requirements_3d.txt"
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)], 
                      check=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install some dependencies: {e}")
        print("Continuing anyway...")
        return True
    except FileNotFoundError:
        print(f"Requirements file not found: {requirements_path}")
        return False

if __name__ == "__main__":
    setup_pipeline()