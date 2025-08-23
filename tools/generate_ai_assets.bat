@echo off
echo.
echo ===============================================================
echo     SANDS OF DUAT - RTX 5070 AI ASSET GENERATOR
echo      Ultra High Quality 4K-8K Egyptian Asset Pipeline  
echo      Optimized for RTX 5070 12GB VRAM + 7800X3D + 32GB RAM
echo ===============================================================
echo.

REM Set window title
title RTX AI Asset Generator - Sands of Duat

REM Navigate to game directory (go up one level since we're in tools/)
cd /d "%~dp0.."

REM Set RTX 5070 optimizations
set CUDA_VISIBLE_DEVICES=0
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024
set GPU_MEMORY_FRACTION=0.95

REM Check if Python is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH!
    echo Please install Python 3.8+ from https://python.org/
    echo Make sure to add Python to your PATH during installation
    pause
    exit /b 1
)

echo [INFO] Python found:
python --version
echo.

REM Check if tools directory exists
if not exist "tools" (
    echo [ERROR] Tools directory not found!
    echo Make sure you're in the correct game directory
    pause
    exit /b 1
)

REM Check if the AI generator script exists
if not exist "tools\ai_asset_generator.py" (
    echo [ERROR] AI asset generator script not found!
    echo Expected: tools\ai_asset_generator.py
    pause
    exit /b 1
)

REM Install RTX-optimized Python dependencies
echo [RTX SETUP] Installing RTX 5070 optimized AI packages...
python -c "import torch, diffusers, PIL" 2>nul
if %errorlevel% neq 0 (
    echo [INSTALL] Installing RTX acceleration packages...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    pip install diffusers transformers accelerate xformers
    pip install requests pillow opencv-python numpy
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install RTX dependencies!
        pause
        exit /b 1
    )
)

echo [SUCCESS] Python dependencies ready!
echo.

REM ===========================================
REM Show menu options
REM ===========================================
echo RTX 5070 High-Performance Generation Options:
echo.
echo 1. 🧪 Test RTX Performance ^& Connection
echo 2. 🎨 Generate 4K Character Sprites (RTX Optimized)
echo 3. 🖼️  Generate 8K Background Environments  
echo 4. 🔧 Generate HD UI Elements Pack
echo 5. ⚔️  Generate 4K Weapons ^& Items
echo 6. 🏛️  Generate Complete Egyptian Asset Pack (4K-8K)
echo 7. 🚀 MEGA GENERATION - Everything Ultra Quality (50+ assets)
echo 8. ⚙️  Custom RTX Generation Settings
echo 9. ❌ Exit
echo.

set /p choice="Enter your choice (1-9): "

REM ===========================================
REM Process user choice
REM ===========================================

if "%choice%"=="1" (
    echo.
    echo [TEST] Testing ComfyUI connection...
    python tools\ai_asset_generator.py test
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo [SINGLE] Generate Single Asset
    echo Available types: character, background, ui_element, weapon
    echo.
    set /p asset_type="Asset type: "
    set /p asset_name="Asset name/description: "
    echo.
    echo [GENERATE] Generating !asset_type!: !asset_name!
    python tools\ai_asset_generator.py generate !asset_type! "!asset_name!"
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo [BATCH] Generating Character Assets...
    python tools\ai_asset_generator.py batch character --count 5
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo [BATCH] Generating UI Element Assets...
    python tools\ai_asset_generator.py batch ui_element --count 5
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo [BATCH] Generating Weapon Assets...
    python tools\ai_asset_generator.py batch weapon --count 5
    goto :end
)

if "%choice%"=="6" (
    echo.
    echo [BATCH] Generating Background Assets...
    python tools\ai_asset_generator.py batch background --count 5
    goto :end
)

if "%choice%"=="7" (
    echo.
    echo [COMPLETE SET] Generating ALL Assets...
    echo This will generate 20+ high-quality Egyptian assets
    echo This may take 15-30 minutes depending on your system
    echo.
    set /p confirm="Continue? (y/n): "
    if /i "!confirm!"=="y" (
        python tools\ai_asset_generator.py all
    ) else (
        echo Generation cancelled.
    )
    goto :end
)

if "%choice%"=="8" (
    echo.
    echo [CUSTOM] Custom Command
    echo Enter Python command arguments for ai_asset_generator.py
    echo Example: batch character --count 3
    echo.
    set /p custom_args="Arguments: "
    python tools\ai_asset_generator.py !custom_args!
    goto :end
)

if "%choice%"=="9" (
    echo Exiting...
    goto :end
)

echo [ERROR] Invalid choice: %choice%

:end
echo.
echo ==========================================
echo NOTE: Generated assets will be saved in:
echo - ai_generated\sprites\
echo - ai_generated\backgrounds\ 
echo - ai_generated\ui\
echo - ai_generated\characters\
echo.
echo Make sure ComfyUI is running before generation!
echo Default ComfyUI URL: http://127.0.0.1:8188
echo ==========================================
echo.
pause