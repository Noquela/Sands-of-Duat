@echo off
echo Opening Godot Editor with Sands of Duat project...
echo.

REM Try common Godot installation paths
set GODOT_PATH=""

REM Check Program Files
if exist "C:\Program Files\Godot\Godot.exe" (
    set GODOT_PATH="C:\Program Files\Godot\Godot.exe"
    goto :found
)

REM Check Program Files (x86)
if exist "C:\Program Files (x86)\Godot\Godot.exe" (
    set GODOT_PATH="C:\Program Files (x86)\Godot\Godot.exe"
    goto :found
)

REM Check Steam installation
if exist "C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.exe" (
    set GODOT_PATH="C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.exe"
    goto :found
)

REM Check user AppData
if exist "%LOCALAPPDATA%\Godot\godot.exe" (
    set GODOT_PATH="%LOCALAPPDATA%\Godot\godot.exe"
    goto :found
)

REM Check if godot is in PATH
where godot >nul 2>&1
if %ERRORLEVEL% == 0 (
    set GODOT_PATH=godot
    goto :found
)

:notfound
echo Godot not found in common locations.
echo Please install Godot or add it to your PATH.
echo.
echo You can download Godot from: https://godotengine.org/download
echo.
echo Once installed, run this script again or manually open:
echo "%~dp0godot\novo-projeto-de-jogo\project.godot"
pause
exit /b 1

:found
echo Found Godot at: %GODOT_PATH%
echo Opening project...
echo.

REM Open the project
%GODOT_PATH% --path "%~dp0godot\novo-projeto-de-jogo"

echo.
echo Instructions for MCP:
echo 1. Once Godot opens, go to Project > Project Settings
echo 2. Go to Plugins tab
echo 3. Enable "Godot MCP" plugin
echo 4. Open the MCP dock from the bottom panel
echo 5. Start the MCP server
echo.
pause