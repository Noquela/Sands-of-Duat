#!/usr/bin/env python3
"""
Alternative launcher for Sands of Duat - Python-based for maximum compatibility.
This launcher works on any system with Python installed.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Launch the game with proper setup."""
    print("=" * 80)
    print("           SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME")
    print("                     Python Game Launcher v1.0")
    print("=" * 80)
    print()
    print("SPRINT 1: Foundation & Core Architecture - COMPLETE")
    print("SPRINT 2: Hades-Style Main Menu - COMPLETE")  
    print("SPRINT 3: Game State Flow & Transitions - COMPLETE")
    print()
    print("Initializing the sacred underworld journey...")
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    main_script = project_root / "src" / "sands_of_duat" / "main.py"
    
    # Check if main script exists
    if not main_script.exists():
        print("ERROR: Main game script not found!")
        print(f"Expected: {main_script}")
        input("Press ENTER to exit...")
        sys.exit(1)
    
    # Check dependencies
    print("Checking dependencies...")
    try:
        import pygame
        print("OK: pygame found")
    except ImportError:
        print("Installing pygame...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("OK: pygame installed")
    
    # Launch the game
    print()
    print("Opening the gates to the Egyptian underworld...")
    print("Game Controls:")
    print("  - ESC: Navigate back / Quit")
    print("  - Menu buttons: Click or use arrow keys + ENTER")
    print("  - F11: Fullscreen")
    print("  - F1: Debug info")
    print()
    print("Starting Sands of Duat...")
    print()
    
    try:
        # Launch the main game
        subprocess.run([sys.executable, str(main_script)], check=True)
        print()
        print("Your journey through the underworld is complete!")
        print("May the gods remember your deeds in the sacred lands.")
        
    except subprocess.CalledProcessError as e:
        print()
        print("The underworld journey encountered challenges.")
        print(f"Exit code: {e.returncode}")
        print("Check the output above for details.")
        
    except KeyboardInterrupt:
        print()
        print("Journey interrupted by the user.")
        
    except Exception as e:
        print()
        print(f"Unexpected error: {e}")
    
    print()
    input("Press ENTER to return to the mortal world...")

if __name__ == "__main__":
    main()