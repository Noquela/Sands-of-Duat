@echo off
echo ================================================
echo           SANDS OF DUAT - Egyptian Roguelike
echo ================================================
echo.
echo Iniciando o jogo...
echo Diretorio: %CD%
echo.

cd /d "C:\Users\Bruno\Documents\Sand of Duat"

echo Verificando arquivos do jogo...
if not exist "main.py" (
    echo ERRO: Arquivo main.py nao encontrado!
    pause
    exit /b 1
)

echo Iniciando Sands of Duat...
echo.
echo Controles:
echo - Clique nos botoes do menu para navegar
echo - Tutorial: Aprenda sobre o jogo e mitologia egipcia
echo - Deck Builder: Construa seus decks de cartas
echo - New Game: Inicie uma nova aventura no combate
echo - F11: Toggle fullscreen 
echo - Alt+F4: Fechar jogo 
echo.

C:\ProgramData\anaconda3\python.exe main.py --windowed --width 3440 --height 1440 

echo.
echo Jogo encerrado. Pressione qualquer tecla para fechar...
pause >nul