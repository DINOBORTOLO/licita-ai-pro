# Adicionar à estrutura existente do banco.py

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

def criar_tabela_historico():
    """Cria tabela para histórico de preços de licitações encerradas"""
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            objeto TEXT NOT NULL,
            categoria TEXT,
            orgao TEXT,
            valor_estimado REAL,
            valor_vencedor REAL,
            valor_ultimo_lance REAL,
            numero_participantes INTEGER,
            data_homologacao DATE,
            modalidade TEXT,
            estado TEXT,
            dispersao_precos REAL,  -- diferença entre maior e menor lance
            desconto_percentual REAL,  -- (estimado - vencedor) / estimado
            empresa_vencedora TEXT,
            arquivo_ata TEXT,  -- caminho para PDF da ata
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Índices para performance nas buscas
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_objeto ON historico_precos(objeto)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_categoria ON historico_precos(categoria)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_data ON historico_precos(data_homologacao)')
    
    conn.commit()
    conn.close()

def inserir_historico(dados: Dict):
    """Insere resultado de licitação no histórico"""
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    
    # Calcular métricas automáticas
    desconto = ((dados['valor_estimado'] - dados['valor_vencedor']) / dados['valor_estimado'] * 100) if dados['valor_estimado'] > 0 else 0
    dispersao = dados.get('maior_lance', 0) - dados.get('menor_lance', dados['valor_vencedor'])
    
    cursor.execute('''
        INSERT INTO historico_precos 
        (objeto, categoria, orgao, valor_estimado, valor_vencedor, valor_ultimo_lance,
         numero_participantes, data_homologacao, modalidade, estado, dispersao_precos,
         desconto_percentual, empresa_vencedora, arquivo_ata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dados['objeto'], dados.get('categoria'), dados['orgao'],
        dados['valor_estimado'], dados['valor_vencedor'], dados.get('valor_ultimo_lance'),
        dados.get('numero_participantes'), dados.get('data_homologacao'),
        dados.get('modalidade'), dados.get('estado'), dispersao,
        desconto, dados.get('empresa_vencedora'), dados.get('arquivo_ata')
    ))
    
    conn.commit()
    conn.close()

def buscar_historico_similar(objeto: str, categoria: str = None, limite: int = 10) -> List[Dict]:
    """Busca licitações similares no histórico"""
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Busca por similaridade no objeto (usando LIKE para palavras-chave)
    palavras_chave = objeto.split()[:3]  # Primeiras 3 palavras
    query_like = '%'.join(palavras_chave)
    
    if categoria:
        cursor.execute('''
            SELECT * FROM historico_precos 
            WHERE (objeto LIKE ? OR categoria = ?)
            AND data_homologacao >= date('now', '-2 years')
            ORDER BY data_homologacao DESC
            LIMIT ?
        ''', (f'%{query_like}%', categoria, limite))
    else:
        cursor.execute('''
            SELECT * FROM historico_precos 
            WHERE objeto LIKE ?
            AND data_homologacao >= date('now', '-2 years')
            ORDER BY data_homologacao DESC
            LIMIT ?
        ''', (f'%{query_like}%', limite))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def calcular_estatisticas_historico(historico: List[Dict]) -> Dict:
    """Calcula estatísticas descritivas do histórico"""
    if not historico:
        return {}
    
    valores_estimados = [h['valor_estimado'] for h in historico if h['valor_estimado']]
    valores_vencedores = [h['valor_vencedor'] for h in historico if h['valor_vencedor']]
    descontos = [h['desconto_percentual'] for h in historico if h['desconto_percentual'] is not None]
    
    import statistics
    
    stats = {
        'media_estimado': statistics.mean(valores_estimados) if valores_estimados else 0,
        'media_vencedor': statistics.mean(valores_vencedores) if valores_vencedores else 0,
        'mediana_vencedor': statistics.median(valores_vencedores) if valores_vencedores else 0,
        'desconto_medio': statistics.mean(descontos) if descontos else 16.0,  # 16% padrão do mercado
        'desconto_min': min(descontos) if descontos else 10.0,
        'desconto_max': max(descontos) if descontos else 25.0,
        'desvio_padrao': statistics.stdev(valores_vencedores) if len(valores_vencedores) > 1 else 0,
        'qtd_amostras': len(historico),
        'preco_minimo': min(valores_vencedores) if valores_vencedores else 0,
        'preco_maximo': max(valores_vencedores) if valores_vencedores else 0,
        'confianca': min(len(historico) / 10, 1.0) * 100  # Confiança baseada em quantidade de dados
    }
    
    # Preço sugerido baseado na mediana (mais robusto que média)
    stats['preco_sugerido'] = stats['mediana_vencedor'] * 0.98  # 2% abaixo da mediana para competitividade
    stats['faixa_recomendada_min'] = stats['preco_sugerido'] * 0.95
    stats['faixa_recomendada_max'] = stats['preco_sugerido'] * 1.02
    
    return stats