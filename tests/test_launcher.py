"""
Test script to verify the .bat file launcher works correctly.
"""

import subprocess
import sys
import os
from pathlib import Path

def test_bat_launcher():
    """Test if the .bat launcher can find and run the game."""
    project_root = Path(__file__).parent
    bat_file = project_root / "Sands_of_Duat.bat"
    
    print("Testing .bat file launcher...")
    print(f"Project root: {project_root}")
    print(f"Bat file exists: {bat_file.exists()}")
    
    if not bat_file.exists():
        print("ERROR: Sands_of_Duat.bat not found!")
        return False
    
    # Test game file exists
    main_py = project_root / "src" / "sands_of_duat" / "main.py"
    print(f"Main game file exists: {main_py.exists()}")
    
    if not main_py.exists():
        print("ERROR: src/sands_of_duat/main.py not found!")
        return False
    
    # Test if we can import the game
    try:
        sys.path.insert(0, str(project_root / "src"))
        from sands_of_duat.core.game_engine import GameEngine
        print("Game engine imports successfully: OK")
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    
    print("\nAll checks passed! The .bat file should work.")
    print("\nTo test the launcher:")
    print("1. Double-click 'Sands_of_Duat.bat' in Windows Explorer")
    print("2. Or run from command prompt: Sands_of_Duat.bat")
    print("\nThe launcher will:")
    print("- Check Python installation")
    print("- Verify game files") 
    print("- Install pygame if needed")
    print("- Launch the game with Egyptian theming")
    
    return True

if __name__ == "__main__":
    test_bat_launcher()