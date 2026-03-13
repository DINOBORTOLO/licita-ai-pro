@echo off
cd /d D:\LICITA_AI_PRO
echo ======================================
echo    LICITA AI PRO - Iniciando...
echo ======================================
echo.
echo Instalando dependências...
pip install -r requirements.txt
echo.
echo Iniciando servidor...
python app.py
pause