@echo off
echo 🏺 Generating AI Egyptian Card Animations
echo ========================================

cd /d "%~dp0\.."
call venv\Scripts\activate.bat

echo Activating virtual environment...
echo Current directory: %CD%

python scripts\generate_ai_animations.py

pause