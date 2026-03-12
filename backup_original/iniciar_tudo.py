#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROBÔ DE LICITAÇÕES NACIONAL - SISTEMA UNIFICADO
Roda coletor + servidor web automaticamente
"""

import subprocess
import sys
import time
import threading
import os

def rodar_robo():
    """Roda o coletor de licitações"""
    print("🤖 Iniciando coletor de licitações...")
    subprocess.run([sys.executable, "robo.py"])

def rodar_web():
    """Roda o servidor web"""
    print("🌐 Iniciando painel web...")
    time.sleep(3)  # Espera o banco criar
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🤖 ROBÔ DE LICITAÇÕES NACIONAL - SISTEMA COMPLETO       ║
    ║                                                              ║
    ║  Iniciando automaticamente:                                  ║
    ║  1. Coletor de licitações (robo.py)                         ║
    ║  2. Servidor web (app.py)                                   ║
    ║                                                              ║
    ║  Acesse: http://localhost:5000                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Roda o coletor em thread separada
    thread_robo = threading.Thread(target=rodar_robo)
    thread_robo.daemon = True
    thread_robo.start()
    
    # Roda o servidor web (principal)
    rodar_web()