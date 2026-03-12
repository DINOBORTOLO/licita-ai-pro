#!/usr/bin/env python3
import sqlite3

print("="*60)
print("  VERIFICADOR DO BANCO DE DADOS")
print("="*60)

try:
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # Lista tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [t[0] for t in cursor.fetchall()]
    print(f"\n📊 Tabelas: {tabelas}")

    if 'licitacoes' in tabelas:
        cursor.execute("SELECT COUNT(*) FROM licitacoes")
        total = cursor.fetchone()[0]
        print(f"📈 Total de licitações: {total}")

        if total > 0:
            cursor.execute("PRAGMA table_info(licitacoes)")
            colunas = [c[1] for c in cursor.fetchall()]
            print(f"📋 Colunas: {', '.join(colunas)}")

            print("\n📝 Últimas 5 licitações:")
            cursor.execute("SELECT id, orgao, objeto, valor FROM licitacoes ORDER BY id DESC LIMIT 5")
            for row in cursor.fetchall():
                print(f"   ID {row[0]}: {row[1][:30] if row[1] else 'N/A'}... | R${row[3]}")
        else:
            print("\n⚠️  Banco vazio! Execute: python popular.py")
    else:
        print("\n❌ Tabela 'licitacoes' não existe!")

    conn.close()

except Exception as e:
    print(f"\n❌ Erro: {e}")

print("\n" + "="*60)