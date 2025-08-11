@echo off
cls
echo 🎬 SANDS OF DUAT - ComfyUI Animation Server
echo ============================================
echo.
echo 🏺 Starting Egyptian Card Animation Pipeline...
echo ⚡ RTX 5070 Optimization: ENABLED
echo 🎨 Egyptian Workflows: LOADED
echo.

cd ComfyUI

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ ComfyUI not properly installed!
    echo Run setup_comfyui.py first to install ComfyUI.
    pause
    exit
)

echo 🚀 Launching ComfyUI Server...
echo 🌐 Server will be available at: http://127.0.0.1:8188
echo.
echo 📋 Egyptian Animation Workflows Available:
echo    • egyptian_creature_animate.json
echo    • egyptian_legendary_animate.json
echo    • egyptian_spell_animate.json  
echo    • egyptian_artifact_animate.json
echo.
echo 🎮 Return to Sands of Duat and use "Animation Forge" to generate cards!
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py --listen 127.0.0.1 --port 8188

echo.
echo 🏺 ComfyUI Server stopped.
pause