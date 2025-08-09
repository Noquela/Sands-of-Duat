
REM AUTOMATIC1111 BATCH GENERATION SCRIPT
REM =====================================
REM 
REM PREREQUISITOS:
REM 1. Automatic1111 instalado e rodando
REM 2. SDXL model carregado
REM 3. API habilitada (--api flag)
REM
REM CONFIGURACOES:
REM - URL: http://127.0.0.1:7860
REM - Model: SDXL Base 1.0
REM - Resolution: 1024x1024
REM - Steps: 30
REM - CFG: 7.5

@echo off
echo INICIANDO BATCH GENERATION AUTOMATIC1111
echo ========================================

REM Verificar se A1111 esta rodando
curl -s http://127.0.0.1:7860/sdapi/v1/progress >nul
if %errorlevel% neq 0 (
    echo ERRO: Automatic1111 nao esta rodando!
    echo Inicie A1111 com: python launch.py --api
    pause
    exit /b 1
)

echo A1111 detectado! Iniciando geracao...

REM Aqui voce pode usar Python script ou ferramenta de batch
echo Use o script Python automatic1111_batch.py
echo Ou importe os prompts manualmente na interface web

pause
