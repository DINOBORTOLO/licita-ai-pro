#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico completo do servidor Flask
"""

import os
import sys
import socket
import subprocess
import sqlite3

DB_PATH = r"D:\robo_licitacoes_nacional\banco.db"

def check_porta():
    """Verifica se porta 5000 está livre"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resultado = sock.connect_ex(('localhost', 5000))
    sock.close()
    return resultado != 0  # True se livre

def check_banco():
    """Verifica banco de dados"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM licitacoes")
        total = cursor.fetchone()[0]
        cursor.execute("PRAGMA table_info(licitacoes)")
        colunas = [row[1] for row in cursor.fetchall()]
        conn.close()
        return True, total, colunas
    except Exception as e:
        return False, 0, str(e)

def check_modulos():
    """Verifica módulos instalados"""
    modulos = ['flask', 'requests', 'bs4', 'sqlite3']
    faltando = []
    for mod in modulos:
        try:
            __import__(mod)
        except ImportError:
            faltando.append(mod)
    return faltando

def main():
    print("=" * 60)
    print("   DIAGNÓSTICO DO SERVIDOR DE LICITAÇÕES")
    print("=" * 60)
    
    # 1. Verifica Python
    print(f"\n[✓] Python: {sys.version.split()[0]}")
    print(f"[✓] Executável: {sys.executable}")
    
    # 2. Verifica porta
    porta_livre = check_porta()
    print(f"\n[{'✓' if porta_livre else '✗'}] Porta 5000: {'LIVRE' if porta_livre else 'OCUPADA'}")
    if not porta_livre:
        print("    → Execute: taskkill /F /IM python.exe")
    
    # 3. Verifica banco
    ok_banco, total, info = check_banco()
    print(f"\n[{'✓' if ok_banco else '✗'}] Banco de dados:")
    if ok_banco:
        print(f"    → Local: {DB_PATH}")
        print(f"    → Registros: {total} licitações")
        print(f"    → Colunas: {len(info)} ({', '.join(info[-3:])}...)")
    else:
        print(f"    → ERRO: {info}")
    
    # 4. Verifica módulos
    faltando = check_modulos()
    print(f"\n[{'✓' if not faltando else '✗'}] Módulos Python:")
    if faltando:
        print(f"    → Faltando: {', '.join(faltando)}")
        print(f"    → Instale: pip install {' '.join(faltando)}")
    else:
        print("    → Todos os módulos instalados")
    
    # 5. Verifica arquivos
    print(f"\n[✓] Arquivos do projeto:")
    arquivos = ['app.py', 'banco.db', 'MODULO_ANALISE_EDITAL.PY']
    for arq in arquivos:
        existe = os.path.exists(os.path.join(r"D:\robo_licitacoes_nacional", arq))
        print(f"    → {arq}: {'OK' if existe else 'FALTANDO'}")
    
    print("\n" + "=" * 60)
    print("   COMANDOS PARA INICIAR:")
    print("=" * 60)
    print("\n1. Simples (recomendado):")
    print("   python app.py")
    print("\n2. Se houver erro de porta:")
    print("   taskkill /F /IM python.exe")
    print("   python app.py")
    print("\n3. Se faltar módulos:")
    print("   pip install flask requests beautifulsoup4")
    print("\n4. Acesso:")
    print("   http://localhost:5000")
    print("=" * 60)
    
    # Pergunta se quer iniciar
    resposta = input("\nDeseja iniciar o servidor agora? (S/N): ")
    if resposta.upper() == 'S':
        print("\nIniciando servidor...\n")
        os.chdir(r"D:\robo_licitacoes_nacional")
        os.system("python app.py || py app.py")

if __name__ == '__main__':
    main()