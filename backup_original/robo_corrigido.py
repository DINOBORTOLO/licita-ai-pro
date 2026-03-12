#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROBÔ DE LICITAÇÕES NACIONAL v2.1
Corrigido para funcionar com app.py unificado
"""

import time
import sys
import os
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================

INTERVALO_BUSCA = 1800  # 30 minutos
MARGEM_MINIMA = 0.20    # 20% (reduzido para capturar mais)
PALAVRAS_ARQUIVO = "keywords.txt"

# ==================== IMPORTAÇÕES ====================

# Banco de dados
try:
    import sqlite3
    BANCO_OK = True
except ImportError:
    BANCO_OK = False
    print("❌ SQLite não disponível")
    sys.exit(1)

# Fontes de dados
try:
    from fontes_hibrido import buscar_todas_fontes
    print("✅ Modo HÍBRIDO ativado (APIs + Demo)")
    MODO = "hibrido"
except ImportError:
    try:
        from fontes import buscar_todas_fontes
        print("✅ Modo API apenas")
        MODO = "api"
    except ImportError:
        print("❌ Nenhuma fonte de dados disponível")
        sys.exit(1)

# ==================== FUNÇÕES DO BANCO ====================

def criar_banco():
    """Cria/verifica estrutura do banco"""
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS licitacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orgao TEXT NOT NULL,
        objeto TEXT NOT NULL,
        valor REAL,
        margem REAL,
        fonte TEXT,
        link TEXT,
        data_publicacao TEXT,
        data_captura TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'nova',
        numero_controle TEXT,
        sequencial TEXT,
        modalidade TEXT,
        situacao TEXT,
        tipo_link TEXT DEFAULT 'busca'
    )
    """)

    # Índices
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_data ON licitacoes(data_captura)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fonte ON licitacoes(fonte)")

    conn.commit()
    conn.close()
    print("✅ Banco de dados pronto")

def salvar_licitacao(orgao, objeto, valor, margem, fonte, link, 
                     data_publicacao, numero_controle=None, 
                     sequencial=None, modalidade=None, situacao=None, 
                     tipo_link='busca'):
    """Salva uma licitação no banco"""
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # Verifica duplicado
    if numero_controle:
        cursor.execute("SELECT id FROM licitacoes WHERE numero_controle = ? AND fonte = ?", 
                      (numero_controle, fonte))
        if cursor.fetchone():
            conn.close()
            return False

    cursor.execute("""
    INSERT INTO licitacoes 
    (orgao, objeto, valor, margem, fonte, link, data_publicacao, 
     numero_controle, sequencial, modalidade, situacao, tipo_link)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (orgao[:500], objeto[:2000], float(valor or 0), float(margem or 0.25), 
          fonte, link, data_publicacao, numero_controle, sequencial, 
          modalidade, situacao, tipo_link))

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

def estatisticas():
    """Retorna estatísticas"""
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM licitacoes")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM licitacoes WHERE date(data_captura) = date('now')")
    hoje = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(valor) FROM licitacoes")
    valor_total = cursor.fetchone()[0] or 0

    conn.close()
    return {"total": total, "hoje": hoje, "valor_total": valor_total}

# ==================== ANÁLISE ====================

def detectar_tipo(objeto):
    """Detecta tipo de licitação pelo objeto"""
    obj_lower = objeto.lower()

    if any(p in obj_lower for p in ["servico", "execucao", "instalacao", "montagem"]):
        return "servico"
    elif any(p in obj_lower for p in ["obra", "construcao", "reforma", "estrutura", "steel frame", "metalica"]):
        return "obra"
    elif any(p in obj_lower for p in ["material construcao", "cimento", "tijolo", "areia"]):
        return "material_construcao"
    elif any(p in obj_lower for p in ["computador", "notebook", "impressora", "informatica"]):
        return "informatica"
    elif any(p in obj_lower for p in ["limpeza", "detergente", "papel", "higienico"]):
        return "limpeza"
    elif any(p in obj_lower for p in ["escolar", "cadeira escolar", "uniforme", "material escolar"]):
        return "escolar"
    elif any(p in obj_lower for p in ["cozinha", "fogao", "freezer", "geladeira", "industrial"]):
        return "cozinha"
    elif any(p in obj_lower for p in ["energia solar", "painel solar", "placa solar"]):
        return "energia_solar"
    else:
        return "produto"

def calcular_margem(valor, tipo="produto"):
    """Calcula margem estimada baseada no tipo"""
    fatores = {
        "produto": 0.65,
        "servico": 0.55,
        "obra": 0.70,
        "material_construcao": 0.60,
        "informatica": 0.75,
        "limpeza": 0.55,
        "escolar": 0.60,
        "cozinha": 0.60,
        "energia_solar": 0.65
    }

    fator = fatores.get(tipo, 0.65)
    custo = valor * fator
    return (valor - custo) / valor if valor > 0 else 0.25

# ==================== PALAVRAS-CHAVE ====================

def carregar_palavras():
    """Carrega palavras-chave"""
    palavras_padrao = [
        "material escolar", "uniforme", "cadeira escolar", "mesa escolar",
        "cozinha industrial", "fogao industrial", "freezer industrial",
        "equipamento esportivo", "informatica", "computador", "notebook",
        "construcao", "reforma", "obra", "estrutura metalica", 
        "steel frame", "light steel frame", "cobertura metalica",
        "galpao", "mezanino", "limpeza", "energia solar", "painel solar"
    ]

    try:
        with open(PALAVRAS_ARQUIVO, 'r', encoding='utf-8') as f:
            palavras = []
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith('#'):
                    palavras.append(linha.lower())
            print(f"✅ {len(palavras)} palavras-chave carregadas")
            return palavras
    except Exception as e:
        print(f"⚠️ Usando palavras padrão: {e}")
        return palavras_padrao

def verificar_compatibilidade(texto, palavras):
    """Verifica se texto contém palavra-chave"""
    if not texto:
        return False, None
    texto_lower = texto.lower()
    for palavra in palavras:
        if palavra in texto_lower:
            return True, palavra
    return False, None

# ==================== ROBÔ PRINCIPAL ====================

class RoboLicitacoes:
    def __init__(self):
        self.palavras_chave = carregar_palavras()
        self.rodadas = 0
        self.novas = 0

    def processar_licitacao(self, lic):
        """Processa uma licitação"""
        objeto = lic.get("objeto", "")
        valor = lic.get("valor", 0) or 0

        if not objeto:
            return False

        # Verifica palavras-chave
        compativel, palavra = verificar_compatibilidade(objeto, self.palavras_chave)
        if not compativel:
            return False

        # Calcula margem
        tipo = detectar_tipo(objeto)
        margem = calcular_margem(valor, tipo)

        if margem < MARGEM_MINIMA:
            return False

        # Salva
        try:
            novo_id = salvar_licitacao(
                orgao=lic.get("orgao", "Não informado"),
                objeto=objeto,
                valor=float(valor),
                margem=float(margem),
                fonte=lic.get("fonte", "DESCONHECIDO"),
                link=lic.get("link", "#"),
                data_publicacao=lic.get("data_publicacao", ""),
                numero_controle=lic.get("numero_controle"),
                sequencial=lic.get("sequencial"),
                modalidade=lic.get("modalidade", "Pregão"),
                situacao=lic.get("situacao", "Aberto"),
                tipo_link=lic.get("tipo_link", "busca")
            )

            if novo_id:
                self.novas += 1
                print(f"\n🎯 #{novo_id}: {palavra.upper()} | R${valor:,.0f} | {margem*100:.0f}% margem")
                print(f"   {objeto[:60]}...")
                return True

        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False

        return False

    def executar_rodada(self):
        """Executa uma rodada de coleta"""
        self.rodadas += 1
        print(f"\n{'='*60}")
        print(f"🤖 RODADA #{self.rodadas} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(f"{'='*60}")

        try:
            licitacoes = buscar_todas_fontes()
        except Exception as e:
            print(f"❌ Erro na coleta: {e}")
            return 0

        print(f"📊 {len(licitacoes)} licitações encontradas nas fontes")

        novas = 0
        for lic in licitacoes:
            if self.processar_licitacao(lic):
                novas += 1

        # Estatísticas
        stats = estatisticas()
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   Total no banco: {stats['total']}")
        print(f"   Capturadas hoje: {stats['hoje']}")
        print(f"   Valor total: R$ {stats['valor_total']:,.0f}")
        print(f"   Novas nesta rodada: {novas}")

        return novas

    def iniciar(self):
        """Inicia o robô"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║           🤖 ROBÔ DE LICITAÇÕES NACIONAL v2.1               ║
║                                                              ║
║  Sistema Unificado - Coletor + Dashboard                    ║
╚══════════════════════════════════════════════════════════════╝
        """)

        criar_banco()

        print(f"\n⚙️  Configurações:")
        print(f"   Margem mínima: {MARGEM_MINIMA*100}%")
        print(f"   Intervalo: {INTERVALO_BUSCA/60} minutos")
        print(f"   Palavras-chave: {len(self.palavras_chave)} termos")
        print(f"   Modo: {MODO.upper()}")

        print("\n🚀 Iniciando coleta...\n")

        try:
            while True:
                self.executar_rodada()

                print(f"\n⏳ Próxima varredura em {INTERVALO_BUSCA/60} minutos...")
                print("   (Pressione Ctrl+C para parar)\n")

                time.sleep(INTERVALO_BUSCA)

        except KeyboardInterrupt:
            print("\n\n🛑 Robô parado pelo usuário")
            stats = estatisticas()
            print(f"\n📈 RESUMO:")
            print(f"   Rodadas: {self.rodadas}")
            print(f"   Novas oportunidades: {self.novas}")
            print(f"   Total no banco: {stats['total']}")
            print(f"\n🌐 Acesse o dashboard: http://localhost:5000")
            print("👋 Até a próxima!")

# ==================== INICIALIZAÇÃO ====================

if __name__ == "__main__":
    robo = RoboLicitacoes()
    robo.iniciar()