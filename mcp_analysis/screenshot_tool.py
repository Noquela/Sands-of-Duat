import pyautogui
import time
import os

def take_screenshot(name, delay=0):
    """Take a screenshot with the given name after an optional delay"""
    if delay > 0:
        time.sleep(delay)
    
    screenshot = pyautogui.screenshot()
    screenshot.save(f'{name}.png')
    print(f'Screenshot saved as {name}.png')

def main():
    # Change to the mcp_analysis directory
    os.chdir(r'C:\Users\Bruno\Documents\Sand of Duat\mcp_analysis')
    
    print("Starting screenshot sequence...")
    print("Make sure the game is running and visible!")
    
    # Wait a moment for the game to be ready
    time.sleep(2)
    
    # Take initial menu screenshot
    take_screenshot("01_main_menu")
    
    print("Screenshots taken! Check the mcp_analysis folder.")

if __name__ == "__main__":
    main()