@echo off
echo.
echo 🏺 SANDS OF DUAT - HADES EGYPTIAN ART GENERATOR 🏺
echo ===================================================
echo Generating beautiful Hades-style Egyptian game assets...
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found, using system Python
)

REM Install requirements if needed
echo 🔧 Installing art generation dependencies...
pip install -r tools\art_requirements.txt

echo.
echo 🎨 Starting Hades-style Egyptian art generation...
echo This will create high-quality assets for your game!
echo.
echo ⏱️ Estimated time: 15-30 minutes (depending on GPU)
echo 💾 Output directory: assets\hades_egyptian_generated\
echo.

python tools\hades_egyptian_art_generator.py

echo.
echo ✅ Art generation complete!
echo 📁 Check the assets\hades_egyptian_generated\ folder
echo 🎮 Assets are ready for use in your game
echo.
pause