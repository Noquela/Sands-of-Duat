@echo off
REM SANDS OF DUAT - PRODUCTION LAUNCHER BATCH FILE
REM =============================================
REM 
REM Easy Windows launcher for Sands of Duat Egyptian Underworld Card Game
REM Double-click this file to start the game with full system integration
REM

title Sands of Duat - Egyptian Underworld Card Game

echo.
echo ===============================================================================
echo                    SANDS OF DUAT - EGYPTIAN UNDERWORLD
echo                         Production Launcher v1.0
echo ===============================================================================
echo.
echo Initializing the sacred underworld journey...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if main game exists
if not exist "src\sands_of_duat\main.py" (
    echo ERROR: Main game script not found
    echo Expected: src\sands_of_duat\main.py
    echo.
    echo Please ensure all game files are present
    echo.
    pause
    exit /b 1
)

REM Install requirements
if exist "requirements.txt" (
    echo Checking game dependencies...
    python -c "import pygame" >nul 2>&1
    if errorlevel 1 (
        echo Installing required dependencies...
        python -m pip install -r requirements.txt
        if errorlevel 1 (
            echo WARNING: Could not install all dependencies
            echo The game may not function properly
            echo.
        )
    ) else (
        echo All dependencies verified!
    )
)

REM Launch the game
echo.
echo Opening the gates to the Egyptian underworld...
echo.

python src\sands_of_duat\main.py

REM Check exit code
if errorlevel 2 (
    echo.
    echo CRITICAL ERROR: Emergency shutdown occurred
    echo Check the logs directory for detailed error information
) else if errorlevel 1 (
    echo.
    echo The underworld journey encountered some challenges
    echo Check the logs if problems persist
) else (
    echo.
    echo Your journey through the underworld is complete
    echo May the gods remember your deeds
)

echo.
echo Press any key to return to the mortal world...
pause >nul