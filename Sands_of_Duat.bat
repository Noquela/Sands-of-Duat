@echo off
REM SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME LAUNCHER
REM =====================================================
REM 
REM Professional Windows launcher for Sands of Duat
REM Sprint-based development with Hades-level polish
REM

title Sands of Duat - Egyptian Underworld Card Game

echo.
echo ===============================================================================
echo           🏺 SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME 🏺
echo                     Professional Game Launcher v2.0
echo ===============================================================================
echo.
echo ⚡ SPRINT 1: Foundation & Core Architecture - COMPLETE
echo 🎯 Next: SPRINT 2 - Hades-Style Main Menu
echo.
echo ✨ Initializing the sacred underworld journey...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo 📥 Please install Python 3.8+ from: https://python.org
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
) else (
    python --version | findstr /C:"Python"
    echo ✅ Python found and ready!
)

REM Check if main game exists
echo 🔍 Verifying game files...
if not exist "src\sands_of_duat\main.py" (
    echo.
    echo ❌ ERROR: Main game script not found
    echo 📍 Expected: src\sands_of_duat\main.py
    echo.
    echo 🔧 Please ensure all game files are present
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Game files verified!
)

REM Check/Install dependencies
echo 🔍 Checking game dependencies...
python -c "import pygame, logging, pathlib, time, enum" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Missing dependencies detected...
    if exist "pyproject.toml" (
        echo 📦 Installing dependencies via pip...
        python -m pip install -e .
        if errorlevel 1 (
            echo ❌ Could not install dependencies automatically
            echo 🔧 Try running: pip install pygame
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo 📦 Installing pygame...
        python -m pip install pygame
        if errorlevel 1 (
            echo ❌ Could not install pygame
            echo 🔧 Please install manually: pip install pygame  
            echo.
            pause
            exit /b 1
        )
    )
) else (
    echo ✅ All dependencies ready!
)

REM Launch the game
echo.
echo 🚪 Opening the gates to the Egyptian underworld...
echo 🎮 Game Controls:
echo    • ESC - Navigate back / Quit
echo    • 1 - Deck Builder    • 2 - Combat    • 3 - Settings
echo    • F11 - Fullscreen    • F1 - Debug info
echo.
echo 🏺 Starting Sands of Duat...
echo.

python src\sands_of_duat\main.py

REM Check exit code and provide feedback
if errorlevel 2 (
    echo.
    echo 💀 CRITICAL ERROR: Emergency shutdown occurred
    echo 📋 Check the console output above for error details
    echo 🔧 If problems persist, check your Python/pygame installation
) else if errorlevel 1 (
    echo.
    echo ⚠️  The underworld journey encountered some challenges
    echo 📋 Check the console output above for details
) else (
    echo.
    echo ✨ Your journey through the underworld is complete
    echo 🏺 May the gods remember your deeds in the sacred lands
)

echo.
echo 🌅 Press any key to return to the mortal world...
pause >nul