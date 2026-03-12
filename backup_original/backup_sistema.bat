@echo off
chcp 65001 >nul
echo ============================================
echo  💾 BACKUP DO SISTEMA DE LICITACOES v1.0
echo ============================================
echo.

set "ORIGEM=D:\robo_licitacoes_nacional"
set "BACKUP=D:\robo_licitacoes_backup_v1"
set "DATA=%date:~0,2%-%date:~3,2%-%date:~6,4%_%time:~0,2%-%time:~3,2%"
set "DATA=%DATA: =0%"

echo 📁 Origem: %ORIGEM%
echo 💾 Destino: %BACKUP%
echo 📅 Data: %DATA%
echo.

:: Cria estrutura de backup
mkdir "%BACKUP%\%DATA%" 2>nul
mkdir "%BACKUP%\%DATA%\templates" 2>nul
mkdir "%BACKUP%\%DATA%\static" 2>nul

echo [1/6] Copiando arquivos Python...
copy "%ORIGEM%\*.py" "%BACKUP%\%DATA%\" >nul
if errorlevel 1 echo ⚠️  Alguns arquivos .py não copiados

echo [2/6] Copiando templates...
xcopy "%ORIGEM%\templates\*.*" "%BACKUP%\%DATA%\templates\" /E /Y /Q >nul 2>&1

echo [3/6] Copiando banco de dados...
copy "%ORIGEM%\banco.db" "%BACKUP%\%DATA%\" >nul 2>&1
if errorlevel 1 echo ⚠️  Banco de dados não encontrado ou em uso

echo [4/6] Copiando configurações...
copy "%ORIGEM%\*.txt" "%BACKUP%\%DATA%\" >nul 2>&1
copy "%ORIGEM%\*.json" "%BACKUP%\%DATA%\" >nul 2>&1
copy "%ORIGEM%\*.env" "%BACKUP%\%DATA%\" >nul 2>&1

echo [5/6] Criando manifesto...
(
echo BACKUP DO SISTEMA DE LICITACOES
echo =================================
echo Data: %date% %time%
echo Versao: v1.0 - Sistema Base Funcional
echo.
echo ARQUIVOS INCLUIDOS:
echo - Modulos Python (robo, app, banco, analisador, fontes)
echo - Templates HTML (dashboard, visualizador, precificador)
echo - Banco de dados SQLite
echo - Configuracoes e palavras-chave
echo.
echo FUNCIONALIDADES:
echo ✓ Coleta de licitacoes (API + Demo)
echo ✓ Dashboard web com estatisticas
echo ✓ Visualizador de editais embutido
echo ✓ Precificacao inteligente
echo ✓ Analise de margem e viabilidade
) > "%BACKUP%\%DATA%\README_BACKUP.txt"

echo [6/6] Criando arquivo ZIP...
powershell -Command "Compress-Archive -Path '%BACKUP%\%DATA%\*' -DestinationPath '%BACKUP%\Sistema_Licitacoes_v1_%DATA%.zip' -Force" >nul 2>&1

echo.
echo ============================================
echo  ✅ BACKUP CONCLUIDO!
echo ============================================
echo.
echo 📂 Local: %BACKUP%\%DATA%\
echo 📦 ZIP: %BACKUP%\Sistema_Licitacoes_v1_%DATA%.zip
echo 📄 Manifesto: README_BACKUP.txt
echo.
echo 💡 Para restaurar: Copie os arquivos de volta para %ORIGEM%
echo.

pause