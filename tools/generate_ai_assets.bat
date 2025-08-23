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
echo RTX 5070 AI Generation Options:
echo.
echo 1. 🔥 Generate Real AI Assets (Uses your RTX 5070!)
echo 2. 🧪 Test RTX 5070 ^& CUDA Setup
echo 3. 📦 Install AI Packages (PyTorch CUDA + Diffusers)
echo 4. 🎨 Generate Egyptian Characters (Stable Diffusion)
echo 5. 🖼️  Generate Egyptian Backgrounds (Ultra Quality)
echo 6. 🏛️  Generate Complete AI Asset Pack
echo 7. ❌ Exit
echo.

set /p choice="Enter your choice (1-7): "

REM ===========================================
REM Process user choice
REM ===========================================

if "%choice%"=="1" (
    echo.
    echo [RTX 5070] Starting REAL AI asset generation...
    python rtx_asset_generator.py
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo [TEST] Testing RTX 5070 and CUDA setup...
    python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo [INSTALL] Installing RTX AI packages...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    pip install diffusers transformers accelerate xformers
    pip install pillow requests
    echo [SUCCESS] AI packages installed!
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo [RTX GEN] Generating Egyptian Characters with Stable Diffusion...
    python rtx_asset_generator.py
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo [RTX GEN] Generating Egyptian Backgrounds with AI...
    python rtx_asset_generator.py
    goto :end
)

if "%choice%"=="6" (
    echo.
    echo [RTX GEN] Generating Complete AI Asset Pack...
    python rtx_asset_generator.py
    goto :end
)

if "%choice%"=="7" (
    echo Exiting RTX AI Generator...
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