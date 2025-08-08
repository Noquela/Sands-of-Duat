#!/usr/bin/env python3
"""
SANDS OF DUAT - GAME LAUNCHER
=============================

Simple, reliable launcher for the Egyptian card game.
This is the main entry point for running the game.
"""

import sys
import os
from pathlib import Path

def launch_game():
    """Launch the Sands of Duat game."""
    # Set up the project root
    project_root = Path(__file__).parent
    main_script = project_root / "src" / "sands_of_duat" / "main.py"
    
    # Verify the main script exists
    if not main_script.exists():
        print(f"ERROR: Game script not found at {main_script}")
        input("Press ENTER to exit...")
        return 1
    
    # Add src to Python path for imports
    src_path = str(project_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Change to the correct directory
    os.chdir(project_root)
    
    # Import and run the main game
    try:
        # Import the main function
        sys.path.insert(0, str(main_script.parent))
        import main
        main.main()
        return 0
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure pygame is installed: pip install pygame")
        input("Press ENTER to exit...")
        return 1
        
    except Exception as e:
        print(f"Error running game: {e}")
        input("Press ENTER to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(launch_game())