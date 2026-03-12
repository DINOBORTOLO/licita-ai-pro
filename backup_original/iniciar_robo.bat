@echo off
echo ==========================================
echo  🤖 ROBÔ DE LICITAÇÕES NACIONAL
echo ==========================================
echo.

echo Iniciando coletor em nova janela...
start cmd /k "cd /d D:\robo_licitacoes_nacional && python robo.py"

echo Aguardando 5 segundos...
timeout /t 5 /nobreak > nul

echo Iniciando servidor web...
start cmd /k "cd /d D:\robo_licitacoes_nacional && python app.py"

echo.
echo ==========================================
echo Acesse: http://localhost:5000
echo ==========================================
pause