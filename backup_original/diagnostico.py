#!/usr/bin/env python3
import sqlite3

print("="*60)
print("  DIAGNÓSTICO DO BANCO")
print("="*60)

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

# Verifica estrutura
cursor.execute("PRAGMA table_info(licitacoes)")
colunas = cursor.fetchall()
print(f"\n📊 Colunas na tabela 'licitacoes':")
for col in colunas:
    print(f"   {col[1]} ({col[2]})")

# Conta total
cursor.execute("SELECT COUNT(*) FROM licitacoes")
total = cursor.fetchone()[0]
print(f"\n📈 Total de registros: {total}")

# Verifica se há dados com margem nula
if total > 0:
    cursor.execute("SELECT COUNT(*) FROM licitacoes WHERE margem IS NULL OR margem = 0")
    sem_margem = cursor.fetchone()[0]
    print(f"⚠️  Registros sem margem: {sem_margem}")

    # Mostra alguns registros
    print(f"\n📝 Primeiros 3 registros:")
    cursor.execute("SELECT id, orgao, objeto, valor, margem FROM licitacoes LIMIT 3")
    for row in cursor.fetchall():
        print(f"   ID {row[0]}: {row[1][:30] if row[1] else 'N/A'}... | Valor: {row[3]} | Margem: {row[4]}")

conn.close()

print("\n" + "="*60)
print("Se 'Registros sem margem' > 0, o app antigo estava filtrando eles fora!")
print("="*60)