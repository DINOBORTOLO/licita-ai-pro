#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migração do banco de dados
Adiciona colunas para análise histórica de preços
"""

import sqlite3
import os

# Caminho correto do seu banco
DB_PATH = r"D:\robo_licitacoes_nacional\banco.db"

def migrar():
    print(f"🔧 Conectando ao banco: {DB_PATH}")
    print("=" * 50)
    
    if not os.path.exists(DB_PATH):
        print(f"❌ ERRO: Banco não encontrado em {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verifica estrutura atual
    cursor.execute("PRAGMA table_info(licitacoes)")
    colunas_existentes = [row[1] for row in cursor.fetchall()]
    print(f"📋 Colunas atuais: {', '.join(colunas_existentes)}")
    print("-" * 50)
    
    novas_colunas = []
    
    # Adiciona valor_fechamento
    if 'valor_fechamento' not in colunas_existentes:
        try:
            cursor.execute("ALTER TABLE licitacoes ADD COLUMN valor_fechamento REAL")
            novas_colunas.append("valor_fechamento")
            print("✅ Coluna 'valor_fechamento' adicionada (PREÇO DE FECHAMENTO)")
        except Exception as e:
            print(f"❌ Erro: {e}")
    else:
        print("⚠️  'valor_fechamento' já existe")
    
    # Adiciona vencedor
    if 'vencedor' not in colunas_existentes:
        try:
            cursor.execute("ALTER TABLE licitacoes ADD COLUMN vencedor TEXT")
            novas_colunas.append("vencedor")
            print("✅ Coluna 'vencedor' adicionada (EMPRESA VENCEDORA)")
        except Exception as e:
            print(f"❌ Erro: {e}")
    else:
        print("⚠️  'vencedor' já existe")
    
    # Adiciona url_edital
    if 'url_edital' not in colunas_existentes:
        try:
            cursor.execute("ALTER TABLE licitacoes ADD COLUMN url_edital TEXT")
            novas_colunas.append("url_edital")
            print("✅ Coluna 'url_edital' adicionada (LINK DO EDITAL)")
        except Exception as e:
            print(f"❌ Erro: {e}")
    else:
        print("⚠️  'url_edital' já existe")
    
    conn.commit()
    
    # Verifica novamente
    cursor.execute("PRAGMA table_info(licitacoes)")
    colunas_finais = [row[1] for row in cursor.fetchall()]
    conn.close()
    
    print("=" * 50)
    if novas_colunas:
        print(f"🚀 SUCESSO! Colunas adicionadas: {', '.join(novas_colunas)}")
    else:
        print("📋 Todas as colunas já existem (nenhuma alteração necessária)")
    print(f"📊 Total de colunas agora: {len(colunas_finais)}")
    print("=" * 50)

if __name__ == '__main__':
    migrar()
    input("\nPressione ENTER para sair...")