@echo off
echo.
echo ================================================================
echo 🏺 SANDS OF DUAT - GENERATE HADES-QUALITY EGYPTIAN ART NOW! 🏺
echo ================================================================
echo.
echo Your RTX 5070 + 32GB RAM setup is PERFECT for AI art generation!
echo Expected quality: Supergiant Games Hades-level excellence
echo.
echo ================================================================
echo QUICK SETUP STEPS:
echo ================================================================
echo.
echo 1. Run this batch file to set up Automatic1111 WebUI
echo 2. Wait 5-10 minutes for setup to complete
echo 3. Open http://localhost:7860 in your browser  
echo 4. Use the prompts from HADES_EGYPTIAN_PROMPTS.txt
echo 5. Generate amazing Egyptian underworld card art!
echo.
echo ================================================================
echo STARTING SETUP...
echo ================================================================
echo.

REM Check if already set up
if exist "AI_Generation\stable-diffusion-webui" (
    echo WebUI already installed! Starting server...
    cd "AI_Generation\stable-diffusion-webui"
    echo.
    echo ================================================================
    echo 🚀 LAUNCHING AI ART GENERATION SERVER
    echo ================================================================
    echo Open http://localhost:7860 when it's ready!
    echo Use prompts from HADES_EGYPTIAN_PROMPTS.txt
    echo.
    start webui-user.bat
    echo.
    echo Server launching in new window...
    echo Check the new command prompt window for progress!
    pause
    exit
)

echo Setting up AI art generation...
mkdir "AI_Generation" 2>nul
cd "AI_Generation"

echo.
echo Downloading Automatic1111 WebUI...
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git

if errorlevel 1 (
    echo.
    echo ERROR: Git not found! Please install Git first:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit
)

cd stable-diffusion-webui

echo.
echo ================================================================
echo ✅ SETUP COMPLETE!
echo ================================================================
echo.
echo Next steps:
echo 1. Double-click webui-user.bat (will appear in new folder)
echo 2. Wait for model download (first time only - ~4GB)
echo 3. Go to http://localhost:7860 in your browser
echo 4. Copy prompts from HADES_EGYPTIAN_PROMPTS.txt
echo 5. Generate AMAZING Egyptian art!
echo.
echo ================================================================
echo 🚀 LAUNCH NOW? (Y/N)
echo ================================================================
set /p choice="Start AI generation server now? "
if /i "%choice%"=="y" (
    echo.
    echo Launching AI art generation server...
    echo Open http://localhost:7860 when ready!
    start webui-user.bat
    echo.
    echo Server starting in new window - check it for progress!
)

echo.
echo ================================================================
echo 🏺 READY TO CREATE HADES-QUALITY EGYPTIAN ART! 🏺
echo ================================================================
pause