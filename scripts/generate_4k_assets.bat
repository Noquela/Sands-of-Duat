@echo off
echo 🏺 SPRINT 2 - 4K Egyptian Art Generation
echo ========================================

cd /d "%~dp0\.."
call venv\Scripts\activate.bat

echo Activating virtual environment...
echo Current directory: %CD%

python scripts\generate_4k_assets.py

pause