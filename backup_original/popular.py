#!/usr/bin/env python3
import sqlite3
import random
from datetime import datetime, timedelta

print("Populando banco de dados...")

orgaos = [
    "Prefeitura Municipal de Sao Paulo - SP",
    "Prefeitura de Belo Horizonte - MG", 
    "Prefeitura de Curitiba - PR",
    "Governo do Estado de Minas Gerais",
    "Universidade Federal de Minas Gerais",
    "Hospital das Clinicas de Porto Alegre",
    "Prefeitura de Recife - PE",
    "Secretaria de Educacao do Rio de Janeiro",
    "Prefeitura de Brasilia - DF",
    "Instituto Federal de Sao Paulo"
]

objetos = [
    ("Aquisicao de 500 cadeiras escolares", 120000),
    ("Fornecimento de material escolar", 85000),
    ("Contratacao de reforma de escolas", 450000),
    ("Aquisicao de cozinha industrial", 180000),
    ("Fornecimento de uniformes", 95000),
    ("Instalacao de cobertura metalica", 320000),
    ("Aquisicao de notebooks", 580000),
    ("Material de limpeza", 45000),
    ("Construcao estrutura metalica", 890000),
    ("Reforma unidade de saude", 650000),
    ("Playground", 78000),
    ("Material construcao", 125000),
    ("Energia solar", 420000),
    ("Fogao industrial", 65000),
    ("Manutencao predial", 95000)
]

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS licitacoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orgao TEXT,
    objeto TEXT,
    valor REAL,
    margem REAL,
    fonte TEXT,
    link TEXT,
    data_publicacao TEXT,
    data_captura TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'nova'
)
""")

hoje = datetime.now()

for i in range(20):
    obj, val = random.choice(objetos)
    valor = val * random.uniform(0.8, 1.2)
    data = (hoje - timedelta(days=random.randint(0,5))).strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO licitacoes (orgao, objeto, valor, margem, fonte, link, data_publicacao, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (random.choice(orgaos), obj, round(valor, 2), 0.25, "DEMO", "https://demo.com/" + str(i), data, "nova"))

conn.commit()
cursor.execute("SELECT COUNT(*) FROM licitacoes")
total = cursor.fetchone()[0]
conn.close()

print(f"✅ {total} licitacoes inseridas!")
print("Execute agora: python app.py")