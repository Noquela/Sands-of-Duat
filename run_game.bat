@echo off
echo Starting Sands of Duat...
echo Changing to game directory...
cd /d "C:\Users\Bruno\Documents\Sand of Duat"
echo Current directory: %CD%
echo Using Python: C:\ProgramData\anaconda3\python.exe
C:\ProgramData\anaconda3\python.exe main.py --dev-mode --windowed
echo.
echo Game ended. Press any key to close...
pause >nul