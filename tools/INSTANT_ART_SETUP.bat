@echo off
echo ================================================================
echo SANDS OF DUAT - INSTANT HADES-QUALITY ART GENERATION SETUP
echo ================================================================
echo Your RTX 5070 + 32GB RAM = PERFECT for AI art generation!
echo.
echo Setting up Automatic1111 WebUI (easiest option)...
echo.
pause

REM Create AI art directory
mkdir "AI_Generation" 2>nul
cd "AI_Generation"

echo Cloning Automatic1111 WebUI...
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

echo.
echo ================================================================
echo SETUP COMPLETE! Now follow these steps:
echo ================================================================
echo.
echo 1. Double-click webui-user.bat to start the interface
echo 2. Wait for it to download the base model (first time only)
echo 3. Go to http://localhost:7860 in your browser
echo 4. Use our Egyptian prompts to generate Hades-quality art!
echo.
echo ================================================================
echo READY-TO-USE EGYPTIAN PROMPTS:
echo ================================================================
echo.
echo LEGENDARY GOD CARD - RA:
echo sands_of_duat_style, egyptian_underworld_art, hades_game_art_quality,
echo majestic egyptian sun god Ra, golden solar disc crown, falcon head,
echo divine solar energy radiating, hieroglyphic symbols, masterpiece quality,
echo supergiant games art style, vibrant rich colors, dramatic lighting
echo.
echo NEGATIVE PROMPT:
echo blurry, low_quality, amateur, modern_elements, photorealistic, 3d_render
echo.
echo ================================================================
pause