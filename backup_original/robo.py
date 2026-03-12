# robo.py - Versão com múltiplas fontes de dados reais
import sys
import os
import sqlite3
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'banco.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def verificar_colunas():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(licitacoes)')
    colunas = {row['name'] for row in cursor.fetchall()}
    conn.close()
    return colunas

def buscar_pncp_api():
    """Busca licitações reais da API do PNCP"""
    try:
        logger.info("🔍 Consultando API do PNCP...")
        
        # Data de hoje e 30 dias atrás
        data_fim = datetime.now().strftime('%Y-%m-%d')
        data_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        url = f"https://pncp.gov.br/api/consulta/v1/contratacoes/publicas?dataInicial={data_inicio}&dataFinal={data_fim}&pagina=1&tamanhoPagina=50"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            licitacoes = []
            for item in data.get('data', []):
                lic = {
                    'identificador': item.get('numeroControlePNCP', 'PNCP-SEM-ID'),
                    'orgao': item.get('orgaoEntidade', {}).get('razaoSocial', 'Órgão não informado'),
                    'objeto': item.get('objetoContratacao', 'Objeto não informado'),
                    'valor_estimado': float(item.get('valorTotalEstimado', 0) or 0),
                    'data_abertura': item.get('dataAberturaProposta') or item.get('dataPublicacaoPncp', datetime.now().strftime('%Y-%m-%d')),
                    'modalidade': item.get('modalidadeContratacaoNome', 'Pregão Eletrônico'),
                    'situacao': 'Aberta' if item.get('situacaoId') == 1 else 'Encerrada',
                    'link_edital': f"https://pncp.gov.br/app/editais/{item.get('numeroControlePNCP', '')}",
                    'fonte': 'PNCP_API'
                }
                licitacoes.append(lic)
            
            logger.info(f"✓ {len(licitacoes)} licitações do PNCP")
            return licitacoes
            
    except urllib.error.HTTPError as e:
        logger.error(f"❌ Erro HTTP PNCP: {e.code} - {e.reason}")
        return []
    except Exception as e:
        logger.error(f"❌ Erro PNCP: {e}")
        return []

def buscar_comprasgov_api():
    """Busca licitações reais do ComprasGov"""
    try:
        logger.info("🔍 Consultando API do ComprasGov...")
        
        url = "https://comprasgov-api.economia.gov.br/licitacao/publica?status=Publicada&pagina=1&tamanho=50"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'chave-api': 'demo-key'  # Algumas APIs precisam de key
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            licitacoes = []
            for item in data.get('content', []):
                lic = {
                    'identificador': f"CGOV-{item.get('id', '0')}",
                    'orgao': item.get('orgao', 'Órgão não informado'),
                    'objeto': item.get('objeto', 'Objeto não informado'),
                    'valor_estimado': float(item.get('valorEstimado', 0) or 0),
                    'data_abertura': item.get('dataAbertura', datetime.now().strftime('%Y-%m-%d')),
                    'modalidade': item.get('modalidade', 'Pregão Eletrônico'),
                    'situacao': item.get('situacao', 'Aberta'),
                    'link_edital': item.get('linkSistemaOrigem', 'https://compras.gov.br'),
                    'fonte': 'COMPRASGOV_API'
                }
                licitacoes.append(lic)
            
            logger.info(f"✓ {len(licitacoes)} licitações do ComprasGov")
            return licitacoes
            
    except Exception as e:
        logger.error(f"❌ Erro ComprasGov: {e}")
        return []

def buscar_todas_fontes():
    """Tenta buscar de todas as fontes disponíveis"""
    todas = []
    
    # Tentar PNCP
    pncp = buscar_pncp_api()
    todas.extend(pncp)
    
    # Tentar ComprasGov
    compras = buscar_comprasgov_api()
    todas.extend(compras)
    
    # Se nenhuma API funcionou, usar dados locais existentes ou demo
    if not todas:
        logger.warning("⚠️ Nenhuma API respondeu, verificando banco local...")
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM licitacoes")
            total = cursor.fetchone()['total']
            conn.close()
            
            if total == 0:
                logger.info("📝 Banco vazio, gerando dados de demonstração...")
                return gerar_demo()
            else:
                logger.info(f"📊 Banco já tem {total} licitações")
                return []
        except:
            return gerar_demo()
    
    return todas

def gerar_demo():
    """Gera dados de demonstração apenas se necessário"""
    import random
    logger.info("🎲 Gerando 5 licitações de demonstração...")
    
    demos = [
        {
            'identificador': f"DEMO-{datetime.now().strftime('%Y%m%d')}-001",
            'orgao': 'PREFEITURA MUNICIPAL DE SÃO PAULO',
            'objeto': 'CADEIRA ESCOLAR EMPILHÁVEL EM AÇO - LOTE 1',
            'valor_estimado': 85000.00,
            'data_abertura': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
            'modalidade': 'Pregão Eletrônico',
            'situacao': 'Aberta',
            'link_edital': 'https://pncp.gov.br/app/editais/001',
            'fonte': 'DEMO'
        },
        {
            'identificador': f"DEMO-{datetime.now().strftime('%Y%m%d')}-002",
            'orgao': 'SECRETARIA DE EDUCAÇÃO DO ESTADO DO RJ',
            'objeto': 'AR CONDICIONADO SPLIT 12000 BTUS - 50 UNIDADES',
            'valor_estimado': 125000.00,
            'data_abertura': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
            'modalidade': 'Pregão Eletrônico',
            'situacao': 'Aberta',
            'link_edital': 'https://pncp.gov.br/app/editais/002',
            'fonte': 'DEMO'
        },
        {
            'identificador': f"DEMO-{datetime.now().strftime('%Y%m%d')}-003",
            'orgao': 'TRIBUNAL DE JUSTIÇA DE MINAS GERAIS',
            'objeto': 'COMPUTADORES DESKTOP I5 8GB RAM SSD 240GB',
            'valor_estimado': 95000.00,
            'data_abertura': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'modalidade': 'Pregão Eletrônico',
            'situacao': 'Aberta',
            'link_edital': 'https://pncp.gov.br/app/editais/003',
            'fonte': 'DEMO'
        },
        {
            'identificador': f"DEMO-{datetime.now().strftime('%Y%m%d')}-004",
            'orgao': 'MINISTÉRIO DA SAÚDE',
            'objeto': 'MATERIAL DE ESCRITÓRIO E PAPELARIA DIVERSOS',
            'valor_estimado': 45000.00,
            'data_abertura': (datetime.now() + timedelta(days=25)).strftime('%Y-%m-%d'),
            'modalidade': 'Pregão Eletrônico',
            'situacao': 'Aberta',
            'link_edital': 'https://pncp.gov.br/app/editais/004',
            'fonte': 'DEMO'
        },
        {
            'identificador': f"DEMO-{datetime.now().strftime('%Y%m%d')}-005",
            'orgao': 'PREFEITURA MUNICIPAL DE CURITIBA',
            'objeto': 'SERVIÇO DE LIMPEZA E CONSERVAÇÃO PREDIAL - 12 MESES',
            'valor_estimado': 180000.00,
            'data_abertura': (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d'),
            'modalidade': 'Pregão Eletrônico',
            'situacao': 'Aberta',
            'link_edital': 'https://pncp.gov.br/app/editais/005',
            'fonte': 'DEMO'
        }
    ]
    return demos

def salvar_inteligente(licitacoes):
    """Salva usando apenas colunas existentes"""
    if not licitacoes:
        return 0
    
    colunas = verificar_colunas()
    logger.info(f"Colunas disponíveis: {colunas}")
    
    conn = get_conn()
    cursor = conn.cursor()
    
    inseridas = 0
    
    for lic in licitacoes:
        try:
            # Mapear apenas campos que existem
            dados = {}
            mapeamento = {
                'identificador': ['identificador', 'id', 'numero', 'sequencial'],
                'orgao': ['orgao', 'orgao_entidade', 'entidade', 'razao_social'],
                'objeto': ['objeto', 'descricao', 'texto_completo', 'titulo', 'objetoContratacao'],
                'valor_estimado': ['valor_estimado', 'valor', 'valorTotalEstimado', 'preco'],
                'data_abertura': ['data_abertura', 'data', 'dataAberturaProposta', 'dataPublicacaoPncp'],
                'modalidade': ['modalidade', 'modalidadeContratacaoNome', 'tipo'],
                'situacao': ['situacao', 'status', 'situacaoId'],
                'link_edital': ['link_edital', 'link', 'linkSistemaOrigem', 'url'],
                'fonte': ['fonte', 'origem', 'source', 'tipo']
            }
            
            for coluna_db, alternativas in mapeamento.items():
                if coluna_db in colunas:
                    for alt in alternativas:
                        if alt in lic and lic[alt] is not None:
                            dados[coluna_db] = lic[alt]
                            break
            
            if not dados or 'identificador' not in dados:
                continue
            
            # Verificar duplicado
            cursor.execute("SELECT id FROM licitacoes WHERE identificador = ?", (dados['identificador'],))
            if cursor.fetchone():
                continue
            
            # Inserir
            cols = list(dados.keys())
            vals = [dados[c] for c in cols]
            ph = ','.join(['?' for _ in cols])
            
            cursor.execute(f"INSERT INTO licitacoes ({','.join(cols)}) VALUES ({ph})", vals)
            inseridas += 1
            logger.info(f"✓ Inserida: {dados['identificador'][:50]}...")
            
        except Exception as e:
            logger.error(f"Erro ao salvar: {e}")
    
    conn.commit()
    conn.close()
    return inseridas

def main():
    print("\n" + "="*70)
    print("  🤖 ROBÔ DE LICITAÇÕES NACIONAL - BUSCA ATIVA")
    print("="*70 + "\n")
    
    # Verificar banco
    try:
        colunas = verificar_colunas()
        if not colunas:
            logger.info("Criando tabela...")
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licitacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identificador TEXT UNIQUE,
                    orgao TEXT,
                    objeto TEXT,
                    valor_estimado REAL,
                    data_abertura TEXT,
                    modalidade TEXT,
                    situacao TEXT,
                    link_edital TEXT,
                    fonte TEXT
                )
            ''')
            conn.commit()
            conn.close()
    except Exception as e:
        logger.error(f"Erro no banco: {e}")
    
    # Buscar dados
    logger.info("🚀 Iniciando busca em fontes oficiais...")
    licitacoes = buscar_todas_fontes()
    
    # Salvar
    if licitacoes:
        total = salvar_inteligente(licitacoes)
        logger.info(f"\n{'='*70}")
        logger.info(f"✅ COLETA CONCLUÍDA: {total} licitações novas")
        logger.info(f"{'='*70}")
        print(f"\n✅ {total} licitações salvas com sucesso!")
    else:
        logger.info("Nenhuma licitação nova para salvar")
        print("\n⚠️ Nenhuma licitação nova encontrada")
    
    print("\n📊 Acesse: http://localhost:5000/dashboard")

if __name__ == '__main__':
    main()