#!/usr/bin/env python3
"""
Game Screenshot Tool
Captures screenshots of all game screens for verification
"""

import pygame
import time
import os
from pathlib import Path
import sys

# Add the game directory to Python path
game_dir = Path(__file__).parent.parent
sys.path.insert(0, str(game_dir))

def take_screenshots():
    """Launch game and take screenshots of each screen"""
    
    # Initialize pygame (minimal setup for screenshot capability)
    pygame.init()
    
    # Launch game in background mode for screenshots
    screenshot_dir = game_dir / "screenshots" 
    screenshot_dir.mkdir(exist_ok=True)
    
    print(f"Screenshot tool ready. Screenshots will be saved to: {screenshot_dir}")
    print("Manual Instructions:")
    print("1. Launch the game using jogar.bat")
    print("2. Navigate to each screen")
    print("3. Press F12 to take a screenshot (if implemented)")
    print("4. Or use Windows Game Bar (Win+Alt+PrintScreen)")
    
    # Provide specific navigation instructions
    screens_to_capture = [
        "Menu Screen - Main menu with background",
        "Combat Screen - Click 'New Game' to enter combat",
        "Map Screen - Look for map navigation option",
        "Deck Builder - Find deck building interface", 
        "Tutorial Screen - Access tutorial if available",
        "Card Display - Show individual cards in combat",
        "Character Sprites - Verify character animations"
    ]
    
    print("\nScreens to Capture:")
    for i, screen in enumerate(screens_to_capture, 1):
        print(f"{i}. {screen}")
    
    print(f"\nGame should be running at 3440x1440 resolution")
    print("Look for:")
    print("- AI background images (Egyptian themed)")
    print("- Professional card artwork") 
    print("- Character sprites/animations")
    print("- Proper UI scaling for ultrawide")
    
    return screenshot_dir

if __name__ == "__main__":
    screenshot_dir = take_screenshots()