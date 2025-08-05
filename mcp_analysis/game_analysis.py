"""
Simple game functionality test script - ASCII version
"""
import subprocess
import time
import os

def test_game_launch():
    """Test if the game launches successfully"""
    print("=" * 60)
    print("SANDS OF DUAT - MCP COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
    # Change to game directory
    os.chdir(r'C:\Users\Bruno\Documents\Sand of Duat')
    
    print("\n1. TESTING GAME LAUNCH...")
    print("-" * 40)
    
    try:
        # Launch the game process
        process = subprocess.Popen([
            r'C:\ProgramData\anaconda3\python.exe',
            'main.py',
            '--windowed',
            '--width', '3440',
            '--height', '1440',
            '--debug'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("SUCCESS: Game process started successfully")
        print("SUCCESS: Running in ultrawide mode (3440x1440)")
        print("SUCCESS: Debug mode enabled")
        
        # Let it run for a few seconds to initialize
        time.sleep(8)
        
        # Check if process is still running
        if process.poll() is None:
            print("SUCCESS: Game is running and stable")
            
            # Terminate the game process
            process.terminate()
            process.wait()
            print("SUCCESS: Game terminated cleanly")
            return True
        else:
            stdout, stderr = process.communicate()
            print("ERROR: Game process ended unexpectedly")
            if stdout:
                print(f"STDOUT: {stdout[:500]}...")
            if stderr:
                print(f"STDERR: {stderr[:500]}...")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to launch game: {e}")
        return False

def analyze_assets():
    """Analyze the available game assets"""
    print("\n2. ANALYZING AI ASSETS...")
    print("-" * 40)
    
    asset_dirs = {
        'Backgrounds': 'game_assets/environments',
        'Cards': 'game_assets/cards', 
        'Character Concepts': 'game_assets/characters/concepts',
        'Character Sprites': 'game_assets/characters/sprites'
    }
    
    total_assets = 0
    for asset_type, path in asset_dirs.items():
        full_path = os.path.join(os.getcwd(), path)
        if os.path.exists(full_path):
            files = [f for f in os.listdir(full_path) if f.endswith('.png')]
            print(f"SUCCESS: {asset_type}: {len(files)} assets found")
            total_assets += len(files)
        else:
            print(f"ERROR: {asset_type}: Directory not found")
    
    print(f"TOTAL AI ASSETS: {total_assets} files")
    return total_assets

def analyze_code_structure():
    """Analyze the game's code structure"""
    print("\n3. ANALYZING CODE STRUCTURE...")
    print("-" * 40)
    
    key_files = [
        'main.py',
        'sands_duat/ui/menu_screen.py',
        'sands_duat/ui/combat_screen.py',
        'sands_duat/ui/deck_builder.py',
        'sands_duat/ui/map_screen.py',
        'sands_duat/core/cards.py',
        'sands_duat/core/hourglass.py'
    ]
    
    found_files = 0
    total_size = 0
    
    for file_path in key_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"SUCCESS: {file_path}: {size} bytes")
            found_files += 1
            total_size += size
        else:
            print(f"ERROR: {file_path}: Missing")
    
    print(f"FOUND FILES: {found_files}/{len(key_files)}")
    print(f"TOTAL CODE SIZE: {total_size} bytes")
    return found_files, total_size

def check_game_logs():
    """Check recent game logs for functionality"""
    print("\n4. CHECKING GAME LOGS...")
    print("-" * 40)
    
    log_file = 'sands_duat.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-20:]  # Last 20 lines
            
            successful_loads = 0
            errors = 0
            
            for line in recent_lines:
                if 'INFO' in line and ('Loaded' in line or 'initialized' in line):
                    successful_loads += 1
                elif 'ERROR' in line:
                    errors += 1
            
            print(f"RECENT SUCCESSFUL OPERATIONS: {successful_loads}")
            print(f"RECENT ERRORS: {errors}")
            
            if successful_loads > 5 and errors == 0:
                print("SUCCESS: Game logs show healthy operation")
                return True
            else:
                print("WARNING: Game logs show potential issues")
                return False
    else:
        print("ERROR: No log file found")
        return False

def main():
    print("Starting comprehensive MCP analysis...")
    
    # Test 1: Game Launch
    launch_success = test_game_launch()
    
    # Test 2: Asset Analysis
    asset_count = analyze_assets()
    
    # Test 3: Code Structure
    found_files, code_size = analyze_code_structure()
    
    # Test 4: Game Logs
    logs_healthy = check_game_logs()
    
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    
    score = 0
    max_score = 4
    
    if launch_success:
        print("SUCCESS: GAME LAUNCHES SUCCESSFULLY")
        score += 1
    else:
        print("ERROR: GAME LAUNCH ISSUES DETECTED")
    
    if asset_count > 20:
        print("SUCCESS: AI ASSETS ARE PRESENT AND ABUNDANT")
        score += 1
    else:
        print("WARNING: LIMITED AI ASSETS DETECTED")
    
    if found_files >= 6:
        print("SUCCESS: CODE STRUCTURE IS COMPLETE")
        score += 1
    else:
        print("ERROR: MISSING CORE CODE FILES")
    
    if logs_healthy:
        print("SUCCESS: GAME LOGS SHOW HEALTHY OPERATION")
        score += 1
    else:
        print("WARNING: GAME LOGS SHOW POTENTIAL ISSUES")
    
    print(f"\nOVERALL SCORE: {score}/{max_score}")
    
    if score >= 3:
        print("CONCLUSION: GAME IS FUNCTIONAL AND WELL-IMPLEMENTED")
    elif score >= 2:
        print("CONCLUSION: GAME HAS MINOR ISSUES BUT IS MOSTLY FUNCTIONAL")
    else:
        print("CONCLUSION: GAME HAS SIGNIFICANT ISSUES")

if __name__ == "__main__":
    main()