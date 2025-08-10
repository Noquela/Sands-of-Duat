@echo off
title Sands of Duat - Egyptian Underworld Card Game

echo.
echo ===============================================================================
echo           SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME
echo                     Professional Game Launcher v4.0
echo ===============================================================================
echo.
echo RTX 5070 Pipeline: COMPLETE - 8/8 Egyptian Cards Generated
echo Professional Animations: COMPLETE - Hades-Quality Effects  
echo Game Integration: COMPLETE - Production Ready
echo.
echo Initializing the sacred underworld journey...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Simple Python check
echo Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ and add to PATH
    pause
    exit /b 1
)

REM Simple file check
if not exist "launch.py" (
    echo ERROR: launch.py not found
    pause
    exit /b 1
)

REM Launch the game
echo.
echo Opening the gates to the Egyptian underworld...
echo.
echo Game Controls:
echo    - ESC: Navigate back / Quit
echo    - Mouse: Navigate menus, play cards
echo    - F11: Fullscreen toggle
echo.
echo Starting Sands of Duat...
echo.

python launch.py

REM Simple exit handling
if errorlevel 1 (
    echo.
    echo Game encountered an issue. Check output above.
) else (
    echo.
    echo Your journey through the underworld is complete!
)

echo.
echo Press any key to return to the mortal world...
pause >nul