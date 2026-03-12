@echo off
echo ==========================================
echo   INICIANDO ROBO DE LICITACOES v6.0
echo ==========================================
echo.

cd /d D:\robo_licitacoes_nacional

echo [1/3] Verificando Python...
python --version || py --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit
)

echo.
echo [2/3] Verificando porta 5000...
netstat -ano | findstr :5000
if %errorlevel% == 0 (
    echo AVISO: Porta 5000 pode estar ocupada
    echo Tentando encerrar processos anteriores...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2 >nul
)

echo.
echo [3/3] Iniciando servidor Flask...
echo Acesse: http://localhost:5000
echo Pressione CTRL+C para parar
echo ==========================================
echo.

:: Tenta iniciar com python ou py
python app.py 2>nul || py app.py

if errorlevel 1 (
    echo.
    echo ERRO AO INICIAR! Verificando dependencias...
    pip install flask requests beautifulsoup4
    echo.
    echo Tentando novamente...
    python app.py 2>nul || py app.py
)

pause