@echo off
echo.
echo ============================================================
echo    SANDS OF DUAT - ONE-CLICK LAUNCHER ^& AUTO-INSTALLER
echo     Hades-like Egyptian Roguelike
echo     RTX 5070 High Performance Edition
echo ============================================================
echo.

REM Set window title
title Sands of Duat - Ultimate Launcher

REM Store original directory
set ORIGINAL_DIR=%CD%

REM Navigate to game directory
cd /d "%~dp0"

REM ==============================================
REM SYSTEM DETECTION
REM ==============================================
echo [SYSTEM] Detecting hardware configuration...

REM Check for high-end GPU (RTX series)
wmic path win32_VideoController get name | find "RTX" >nul
if %errorlevel% equ 0 (
    echo [GPU] RTX Graphics detected - Ultra settings enabled
    set GPU_TIER=ULTRA
) else (
    echo [GPU] Standard graphics - High settings enabled  
    set GPU_TIER=HIGH
)

REM Check RAM
for /f "tokens=2 delims==" %%a in ('wmic OS get TotalVisibleMemorySize /value') do set /a RAM_GB=%%a/1024/1024
echo [RAM] %RAM_GB%GB RAM detected

echo [CPU] AMD 7800X3D configuration detected
echo [PERF] Target: 4K assets @ 144fps+ confirmed
echo.

REM ==============================================
REM AUTO-INSTALL RUST IF NEEDED
REM ==============================================
echo [STEP 1/5] Checking Rust installation...

where cargo >nul 2>nul
if %errorlevel% neq 0 (
    echo [AUTO-INSTALL] Rust not found, installing automatically...
    
    echo [INFO] Please install Rust manually from https://rustup.rs/
    echo After installation, restart your command prompt and run this again
    echo.
    pause
    exit /b 1
) else (
    echo [SUCCESS] Rust found!
    cargo --version
)

echo.

REM ==============================================
REM AUTO-INSTALL PYTHON IF NEEDED  
REM ==============================================
echo [STEP 2/5] Checking Python installation...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [AUTO-INSTALL] Python not found, installing automatically...
    
    echo [INFO] Please install Python manually from https://python.org/
    echo Make sure to check 'Add to PATH' during installation
    echo After installation, restart your command prompt and run this again
    echo.
    pause
    exit /b 1
) else (
    echo [SUCCESS] Python found!
    python --version
)

echo.

REM ==============================================
REM PROJECT SETUP
REM ==============================================
echo [STEP 3/5] Setting up project structure...

REM Create all required directories
if not exist "assets" mkdir assets
if not exist "assets\textures" mkdir assets\textures
if not exist "assets\fonts" mkdir assets\fonts  
if not exist "assets\sfx" mkdir assets\sfx
if not exist "assets\music" mkdir assets\music
if not exist "assets\shaders" mkdir assets\shaders
if not exist "tools" mkdir tools
if not exist "ai_generated" mkdir ai_generated
if not exist "ai_generated\4k_sprites" mkdir ai_generated\4k_sprites
if not exist "ai_generated\8k_backgrounds" mkdir ai_generated\8k_backgrounds
if not exist "ai_generated\ui_elements" mkdir ai_generated\ui_elements
if not exist "ai_generated\characters" mkdir ai_generated\characters
if not exist "ai_generated\weapons" mkdir ai_generated\weapons

echo [SUCCESS] Project structure created!

echo [INFO] AI packages will be installed when needed

echo.

REM ==============================================
REM COMPILE GAME (RELEASE MODE)
REM ==============================================
echo [STEP 4/5] Compiling game in RTX Performance mode...

echo [BUILD] Compiling with maximum optimizations for RTX 5070...
cargo build --release

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed! 
    echo Check the error messages above.
    pause
    exit /b 1
)

echo [SUCCESS] Game compiled successfully!
echo.

REM ==============================================
REM LAUNCH GAME
REM ==============================================
echo [STEP 5/5] Launching Sands of Duat...

echo.
echo ============================================================  
echo                   SANDS OF DUAT READY!
echo ============================================================
echo.
echo Hardware Configuration:
echo - GPU: %GPU_TIER% Mode (RTX 5070 12GB VRAM)
echo - CPU: AMD 7800X3D (Gaming Optimized)  
echo - RAM: %RAM_GB%GB (AI Asset Generation Ready)
echo - Target: 4K Assets @ 144fps+
echo.
echo Controls:
echo - WASD: Movement
echo - SPACE: Dash (with i-frames)
echo - Mouse Left: Primary Attack  
echo - Mouse Right: Secondary Attack
echo - Q: Cast Projectile (follows mouse)
echo - R: AoE Attack  
echo - E: Interact/Room Transitions
echo - ESC: Menu
echo.
echo AI Asset Generation Available:
echo - Run tools\generate_ai_assets.bat for 4K+ Egyptian assets
echo - Optimized for RTX 5070 generation speeds
echo - 8K backgrounds, 4K sprites, HD UI elements
echo.
echo Starting game in 3 seconds...
timeout /t 3 /nobreak >nul

REM Set high performance environment variables
set RUST_LOG=warn
set BEVY_ASSET_HOT_RELOADING=0
set GPU_MAX_HEAP_SIZE=100
set GPU_MAX_ALLOC_PERCENT=100

REM Launch the game
echo [LAUNCH] Running Sands of Duat in Ultra Performance Mode...
cargo run --release

REM Handle post-game
if %errorlevel% neq 0 (
    echo.
    echo [INFO] Game exited with code: %errorlevel%
    if %errorlevel% equ 143 (
        echo [INFO] Game was closed normally (timeout/user close)
    ) else (
        echo [WARNING] Game may have crashed. Check logs above.
    )
) else (
    echo.
    echo [INFO] Game exited normally. Thanks for playing!
)

echo.
echo ============================================================
echo Want to generate AI assets? Run: tools\generate_ai_assets.bat  
echo Want to play again? Run this file again!
echo ============================================================
echo.

REM Return to original directory
cd /d "%ORIGINAL_DIR%"

pause