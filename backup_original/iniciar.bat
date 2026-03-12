@echo off
chcp 65001 >nul
echo ==========================================
echo  🤖 INICIADOR DO SISTEMA DE LICITAÇÕES
echo ==========================================
echo.

REM Verifica pasta
echo 📁 Verificando pasta...
if not exist "banco.db" (
    echo ❌ ERRO: banco.db nao encontrado!
    echo 📂 Voce esta em: %CD%
    pause
    exit /b 1
)

echo ✅ Pasta correta encontrada

REM Verifica Python
echo 🐍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado!
    echo 💡 Instale Python em: https://python.org
    pause
    exit /b 1
)

echo ✅ Python OK

REM Mata processos anteriores (se houver)
echo 🧹 Limpando processos anteriores...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *flask*" 2>nul
ping -n 2 127.0.0.1 >nul

echo ✅ Limpo

REM Verifica qual app usar
if exist "app_emergencia.py" (
    set APP=app_emergencia.py
    echo 🚀 Usando: app_emergencia.py (versao emergencia)
) else (
    if exist "app.py" (
        set APP=app.py
        echo 🚀 Usando: app.py (versao normal)
    ) else (
        echo ❌ Nenhum app.py encontrado!
        pause
        exit /b 1
    )
)

echo.
echo ==========================================
echo  🌐 INICIANDO SERVIDOR...
echo ==========================================
echo.
echo 📍 Acesse: http://localhost:5000
echo 🛑 Para parar: FECHE ESTA JANELA
echo.
echo Aguardando inicializacao...
echo.

REM Inicia o servidor
python %APP%

echo.
echo ==========================================
echo  Servidor encerrado
echo ==========================================
pause