@echo off
chcp 65001 >nul
echo ==========================================
echo  POPULANDO BANCO DE DADOS
echo ==========================================
echo.

if not exist "banco.db" (
    echo ERRO: banco.db nao encontrado!
    pause
    exit /b 1
)

echo Criando arquivo temporario...

(
echo import sqlite3
echo import random
echo from datetime import datetime, timedelta
echo.
echo ORGAOS = [
echo     "Prefeitura Municipal de Sao Paulo - SP",
echo     "Prefeitura de Belo Horizonte - MG", 
echo     "Prefeitura de Curitiba - PR",
echo     "Governo do Estado de Minas Gerais",
echo     "Universidade Federal de Minas Gerais",
echo     "Hospital das Clinicas de Porto Alegre",
echo     "Prefeitura de Recife - PE",
echo     "Secretaria de Educacao do Rio de Janeiro",
echo     "Prefeitura de Brasilia - DF",
echo     "Instituto Federal de Sao Paulo"
echo ]
echo.
echo OBJETOS = [
echo     ("Aquisicao de 500 cadeiras escolares", 120000),
echo     ("Fornecimento de material escolar", 85000),
echo     ("Contratacao de reforma de escolas", 450000),
echo     ("Aquisicao de cozinha industrial", 180000),
echo     ("Fornecimento de uniformes", 95000),
echo     ("Instalacao de cobertura metalica", 320000),
echo     ("Aquisicao de notebooks", 580000),
echo     ("Material de limpeza", 45000),
echo     ("Construcao estrutura metalica", 890000),
echo     ("Reforma unidade de saude", 650000),
echo     ("Playground", 78000),
echo     ("Material construcao", 125000),
echo     ("Energia solar", 420000),
echo     ("Fogao industrial", 65000),
echo     ("Manutencao predial", 95000)
echo ]
echo.
echo print("Conectando ao banco...")
echo conn = sqlite3.connect("banco.db")
echo cursor = conn.cursor()
echo.
echo cursor.execute("""
echo CREATE TABLE IF NOT EXISTS licitacoes(
echo     id INTEGER PRIMARY KEY AUTOINCREMENT,
echo     orgao TEXT,
echo     objeto TEXT,
echo     valor REAL,
echo     margem REAL,
echo     fonte TEXT,
echo     link TEXT,
echo     data_publicacao TEXT,
echo     data_captura TEXT DEFAULT CURRENT_TIMESTAMP,
echo     status TEXT DEFAULT 'nova'
echo )
echo """)
echo.
echo hoje = datetime.now()
echo print("Inserindo 20 licitacoes...")
echo.
echo for i in range(20):
echo     obj, val = random.choice(OBJETOS)
echo     valor = val * random.uniform(0.8, 1.2)
echo     data = (hoje - timedelta(days=random.randint(0,5))).strftime("%%Y-%%m-%%d")
echo     cursor.execute("""
echo         INSERT INTO licitacoes (orgao, objeto, valor, margem, fonte, link, data_publicacao, status)
echo         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
echo     """, (random.choice(ORGAOS), obj, round(valor, 2), 0.25, "DEMO", "https://demo.com/" + str(i), data, "nova"))
echo.
echo conn.commit()
echo cursor.execute("SELECT COUNT(*) FROM licitacoes")
echo total = cursor.fetchone()[0]
echo conn.close()
echo print(f"✅ {total} licitacoes inseridas com sucesso!")
) > temp_popular.py

echo Executando Python...
python temp_popular.py

del temp_popular.py

echo.
echo ==========================================
echo  PRONTO! Agora execute: python app.py
echo  Acesse: http://localhost:5000/
echo ==========================================
pause