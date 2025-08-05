@echo off
chcp 65001 >nul
echo ================================================
echo           SANDS OF DUAT - Egyptian Roguelike
echo                  Com Assets AI Profissionais
echo ================================================
echo.
echo 🎮 Iniciando o jogo...
echo 📁 Local: %CD%
echo.

REM Verificar se estamos no diretório correto
if not exist "main.py" (
    echo ❌ ERRO: Arquivo main.py não encontrado!
    echo    Certifique-se de que está no diretório correto do jogo.
    pause
    exit /b 1
)

REM Verificar se Python está disponível
"C:\ProgramData\anaconda3\python.exe" --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado em C:\ProgramData\anaconda3\
    echo    Verifique se o Anaconda está instalado corretamente.
    pause
    exit /b 1
)

REM Verificar assets AI
if not exist "game_assets\cards\mummys_wrath.png" (
    echo ⚠️  AVISO: Assets AI podem estar faltando
    echo    O jogo funcionará, mas pode usar placeholders.
)

echo ✅ Verificações concluídas
echo.
echo 🎯 Controles do Jogo:
echo    • Clique nos botões do menu para navegar
echo    • Tutorial: Aprenda sobre o jogo e mitologia egípcia  
echo    • Deck Builder: Construa seus decks de cartas
echo    • New Game: Inicie uma nova aventura no combate
echo    • F11: Alternar tela cheia
echo    • Alt+F4: Fechar jogo
echo.
echo 🚀 Iniciando Sands of Duat com assets AI profissionais...
echo.

REM Iniciar o jogo em modo janela ultrawide
"C:\ProgramData\anaconda3\python.exe" main.py --windowed --width 3440 --height 1440 --debug

echo.
echo 🎮 Jogo encerrado. Pressione qualquer tecla para fechar...
pause >nul