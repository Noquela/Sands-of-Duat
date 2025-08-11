@echo off
echo 🏺 Sands of Duat - AI Animation Setup
echo =====================================

cd /d "%~dp0\.."
call venv\Scripts\activate.bat

echo Activating virtual environment...
echo Current directory: %CD%

python scripts\setup_ai_generation.py

pause