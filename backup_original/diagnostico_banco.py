
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO RÁPIDO DO BANCO
Execute para verificar o estado do banco de dados
"""

import sqlite3
import os

DB_PATH = 'banco.db'

print("="*60)
print("🔍 DIAGNÓSTICO DO BANCO DE DADOS")
print("="*60)

if not os.path.exists(DB_PATH):
    print(f"❌ Banco não encontrado: {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Verifica tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = [t[0] for t in cursor.fetchall()]
print(f"
📊 Tabelas encontradas: {tabelas}")

if 'licitacoes' not in tabelas:
    print("❌ Tabela 'licitacoes' não existe!")
    conn.close()
    exit(1)

# 2. Verifica estrutura
cursor.execute("PRAGMA table_info(licitacoes)")
colunas = cursor.fetchall()
print(f"
📋 Estrutura da tabela 'licitacoes':")
for col in colunas:
    print(f"   {col[1]} ({col[2]})")

# 3. Conta registros
cursor.execute("SELECT COUNT(*) FROM licitacoes")
total = cursor.fetchone()[0]
print(f"
📈 Total de registros: {total}")

if total > 0:
    # 4. Mostra últimos registros
    print(f"
📝 Últimos 5 registros:")
    cursor.execute("SELECT id, orgao, objeto, valor, data_captura FROM licitacoes ORDER BY id DESC LIMIT 5")
    for row in cursor.fetchall():
        print(f"   ID {row[0]}: {row[1][:30] if row[1] else 'N/A'}... | R${row[3]} | {row[4]}")
else:
    print("
⚠️  Banco está VAZIO - Execute o robo.py para popular")

conn.close()
print("
" + "="*60)