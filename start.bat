@echo off
cd /d D:\LICITA_AI_PRO
echo ======================================
echo    LICITA AI PRO - Iniciando...
echo ======================================
python -c "import flask" 2>nul || pip install flask
echo.
python app.py
pause