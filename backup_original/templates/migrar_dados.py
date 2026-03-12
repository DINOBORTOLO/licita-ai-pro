import sqlite3
import json
from datetime import datetime, timedelta
import random

def popular_dados_demo():
    """Popula a tabela de histórico com dados demonstrativos realistas"""
    
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    
    # Dados demo baseados em padrões reais de licitações brasileiras
    dados_demo = [
        {
            'objeto': 'CADEIRA ESCOLAR EMPILHÁVEL',
            'categoria': 'MOBILIÁRIO EDUCACIONAL',
            'orgao': 'PREFEITURA MUNICIPAL DE SÃO PAULO',
            'valor_estimado': 85000.00,
            'valor_vencedor': 72250.00,
            'valor_ultimo_lance': 72500.00,
            'numero_participantes': 8,
            'data_homologacao': '2024-01-15',
            'modalidade': 'PREGÃO ELETRÔNICO',
            'estado': 'SP',
            'empresa_vencedora': 'MOVEIS EDUCAÇÃO LTDA'
        },
        {
            'objeto': 'CADEIRA ESCOLAR EMPILHÁVEL',
            'categoria': 'MOBILIÁRIO EDUCACIONAL',
            'orgao': 'SECRETARIA DE EDUCAÇÃO DO RJ',
            'valor_estimado': 92000.00,
            'valor_vencedor': 75440.00,
            'valor_ultimo_lance': 76000.00,
            'numero_participantes': 12,
            'data_homologacao': '2024-02-20',
            'modalidade': 'PREGÃO ELETRÔNICO',
            'estado': 'RJ',
            'empresa_vencedora': 'MOBILIÁRIO ESCOLAR S.A.'
        },
        {
            'objeto': 'CADEIRA ESCOLAR EMPILHÁVEL',
            'categoria': 'MOBILIÁRIO EDUCACIONAL',
            'orgao': 'PREFEITURA DE BELO HORIZONTE',
            'valor_estimado': 78000.00,
            'valor_vencedor': 65500.00,
            'valor_ultimo_lance': 65800.00,
            'numero_participantes': 6,
            'data_homologacao': '2024-03-10',
            'modalidade': 'PREGÃO ELETRÔNICO',
            'estado': 'MG',
            'empresa_vencedora': 'MOVEIS EDUCAÇÃO LTDA'
        },
        {
            'objeto': 'CADEIRA ESCOLAR EMPILHÁVEL',
            'categoria': 'MOBILIÁRIO EDUCACIONAL',
            'orgao': 'SECRETARIA DE EDUCAÇÃO DO RS',
            'valor_estimado': 88000.00,
            'valor_vencedor': 73000.00,
            'valor_ultimo_lance': 73500.00,
            'numero_participantes': 9,
            'data_homologacao': '2024-04-05',
            'modalidade': 'PREGÃO ELETRÔNICO',
            'estado': 'RS',
            'empresa_vencedora': 'SUL MOVEIS EDUCACIONAIS'
        },
        {
            'objeto': 'CADEIRA ESCOLAR EMPILHÁVEL',
            'categoria': 'MOBILIÁRIO EDUCACIONAL',
            'orgao': 'PREFEITURA DE CURITIBA',
            'valor_estimado': 95000.00,
            'valor_vencedor': 80750.00,
            'valor_ultimo_lance': 81000.00,
            'numero_participantes': 11,
            'data_homologacao': '2024-05-12',
            'modalidade': 'PREGÃO ELETRÔNICO',
            'estado': 'PR',
            'empresa_vencedora': 'PARANÁ MOVEIS LTDA'
        },
        # Adicionar mais variedade de produtos
        {
            'objeto': 'AR CONDICIONADO SPLIT 12000 BTUS',
            'categoria': 'EQUIPAMENTOS DE INFORMÁTICA',
            'orgao': 'TRIBUNAL DE JUSTIÇA DE SP',
            'valor_estimado': 45000.00,
            'valor_vencedor': 38250.00,
            'numero_participantes': 7,
            'data_homologacao': '2024-01-20',
            'modalidade': 'PREGÃO ELETRÔNICO',
            'estado': 'SP'
        },
        {
            'objeto': 'AR CONDICIONADO SPLIT 12000 BTUS',
            'categoria': 'EQUIPAMENTOS DE INFORMÁTICA',
            'orgao': 'MINISTÉRIO DA SAÚDE',
            'valor_estimado': 52000.00,
            'valor_vencedor': 44200.00,
            'numero_participantes': 10,
            'data_homologacao': '2024-03-15',
            'modalidade': 'PREGÃO ELETRÔNICO',
            'estado': 'DF'
        }
    ]
    
    from banco import inserir_historico
    
    for dado in dados_demo:
        try:
            inserir_historico(dado)
            print(f"✓ Inserido: {dado['objeto']} - {dado['orgao']}")
        except Exception as e:
            print(f"✗ Erro ao inserir {dado['objeto']}: {e}")
    
    print("\n✅ Base de dados histórica populada com sucesso!")
    print(f"Total de registros: {len(dados_demo)}")

if __name__ == '__main__':
    popular_dados_demo()