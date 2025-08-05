import pyautogui
import pygetwindow as gw
import time
import os

def find_game_window():
    """Find the Sands of Duat game window"""
    windows = gw.getAllWindows()
    
    # Look for windows that might contain the game
    game_keywords = ['sands', 'duat', 'pygame', 'python']
    
    print("Available windows:")
    for window in windows:
        print(f"  - {window.title}")
        
    # Try to find the game window
    for window in windows:
        title_lower = window.title.lower()
        for keyword in game_keywords:
            if keyword in title_lower:
                print(f"Found potential game window: {window.title}")
                return window
    
    return None

def take_game_screenshot(name, delay=0):
    """Take a screenshot of the game window specifically"""
    if delay > 0:
        time.sleep(delay)
    
    # Try to find and focus the game window
    game_window = find_game_window()
    
    if game_window:
        try:
            # Focus the window
            game_window.activate()
            time.sleep(1)  # Wait for window to become active
            
            # Take screenshot of the specific window region
            screenshot = pyautogui.screenshot(region=(game_window.left, game_window.top, 
                                                   game_window.width, game_window.height))
            screenshot.save(f'{name}.png')
            print(f'Game window screenshot saved as {name}.png')
            print(f'Window size: {game_window.width}x{game_window.height}')
            return True
        except Exception as e:
            print(f"Error taking window screenshot: {e}")
            return False
    else:
        # Fallback to full screen screenshot
        print("Game window not found, taking full screen screenshot")
        screenshot = pyautogui.screenshot()
        screenshot.save(f'{name}.png')
        print(f'Full screen screenshot saved as {name}.png')
        return True

def main():
    # Change to the mcp_analysis directory
    os.chdir(r'C:\Users\Bruno\Documents\Sand of Duat\mcp_analysis')
    
    print("Starting game screenshot sequence...")
    
    # Wait a moment
    time.sleep(2)
    
    # Take initial menu screenshot
    success = take_game_screenshot("02_main_menu_focused")
    
    if success:
        print("Screenshot sequence complete!")
    else:
        print("Screenshot sequence failed!")

if __name__ == "__main__":
    main()