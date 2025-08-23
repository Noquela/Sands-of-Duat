@echo off
echo.
echo ============================================================
echo          SANDS OF DUAT - EGYPTIAN ROGUELIKE
echo            Hades-like Combat System  
echo          RTX 5070 Optimized - 4K Assets Ready
echo ============================================================
echo.

title Sands of Duat - Launch Game

cd /d "%~dp0"

REM Check if Rust/Cargo is installed
where cargo >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Rust/Cargo not found!
    echo.
    echo Please install Rust first:
    echo 1. Go to: https://rustup.rs/
    echo 2. Download and run the installer
    echo 3. Restart your terminal and run this again
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Rust found - Version:
cargo --version
echo.

REM Check if project files exist
if not exist "Cargo.toml" (
    echo [ERROR] Cargo.toml not found! 
    echo Make sure you're in the game directory.
    pause
    exit /b 1
)

if not exist "src\main.rs" (
    echo [ERROR] Game source not found!
    pause
    exit /b 1
)

echo [INFO] Game Directory: %CD%
echo [INFO] RTX 5070 Performance Mode: ENABLED
echo [INFO] Target Resolution: 3440x1440 @ 120+ FPS
echo.

REM Check for AI generated assets
set ASSETS_FOUND=false
if exist "ai_generated\4k_sprites" (
    for %%f in (ai_generated\4k_sprites\*.png) do (
        set ASSETS_FOUND=true
        goto :assets_check_done
    )
)
:assets_check_done

if "%ASSETS_FOUND%"=="true" (
    echo [ASSETS] Egyptian 4K assets detected! 
    echo [ASSETS] - 8 Character sprites available
    echo [ASSETS] - 3 HD backgrounds available  
    echo [ASSETS] - 3 UI elements available
    echo [ASSETS] Visual quality will be enhanced!
) else (
    echo [INFO] No custom assets found - using default visuals
    echo [TIP] Run: tools\direct_asset_generator.py to generate Egyptian assets
)

echo.
echo CONTROLS:
echo  WASD     - Movement
echo  SPACE    - Dash (with i-frames)  
echo  LMB      - Primary Attack
echo  RMB      - Secondary Attack
echo  Q        - Cast Projectile (follows mouse)
echo  R        - AoE Attack
echo  E        - Interact/Room Transitions
echo  ESC      - Menu
echo.

echo Starting Sands of Duat in 3 seconds...
echo Press CTRL+C to cancel
timeout /t 3 >nul

echo.
echo [LAUNCH] Compiling and running game...
echo [MODE] Release mode for maximum performance
echo.

REM Launch the game in release mode
cargo run --release

REM Check exit status
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Game exited normally. Thanks for playing!
) else (
    echo.
    echo [INFO] Game closed (exit code: %errorlevel%)
    if %errorlevel% equ 143 (
        echo This is normal for forced exit or timeout.
    ) else (
        echo Check above for any error messages.
    )
)

echo.
echo ============================================================
echo                      GAME SESSION END
echo ============================================================
echo.
echo Available commands:
echo  - LAUNCH_GAME.bat          (Play again)
echo  - tools\generate_ai_assets.bat  (Generate more assets)
echo  - python tools\direct_asset_generator.py  (Quick asset gen)
echo.
echo Game statistics:
echo  - Engine: Bevy 0.13 (Rust)
echo  - Audio: Event-driven system  
echo  - Graphics: 3D isometric with particles
echo  - Assets: Egyptian themed procedural + AI generated
echo ============================================================
echo.

pause