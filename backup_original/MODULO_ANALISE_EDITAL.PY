#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULO_ANALISE_EDITAL.PY - Análise Profunda de Editais
Extrai e estrutura todas as informações críticas para decisão de compra
"""

import sqlite3
import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json

# ============================================================================
# CONFIGURAÇÕES DE BUSCA DE EDITAIS
# ============================================================================

PORTAIS_BUSCA = {
    'pncp': {
        'nome': 'Portal Nacional de Contratações Públicas',
        'url_base': 'https://pncp.gov.br/app/editais',
        'api_base': 'https://pncp.gov.br/api/pncp/v1/orgaos',
        'padrao_id': r'(\d{14})-(\d{4})'  # CNPJ:ANO
    },
    'comprasnet': {
        'nome': 'ComprasNet',
        'url_base': 'http://www.comprasnet.gov.br/seguro/licitacoes/licitacao',
        'padrao_id': r'(\d{5})/(\d{4})'  # Número/Ano
    },
    'licitacoes_e': {
        'nome': 'Licitações-e',
        'url_base': 'https://www.licitacoes-e.com.br/aop/pesquisar-licitacao.aop',
        'padrao_id': r'(\d{4})\.(\d{3})'  # Ano.Número
    }
}

# ============================================================================
# FUNÇÕES DE BUSCA DE EDITAL
# ============================================================================

def buscar_edital_original(objeto, orgao, data_pub=None, valor_estimado=None):
    """
    Busca o edital original em múltiplas fontes
    Retorna dicionário com URLs e metadados
    """
    resultados = []
    
    # Busca 1: PNCP (mais completo)
    try:
        url_pncp = buscar_pncp(objeto, orgao, data_pub)
        if url_pncp:
            resultados.append({
                'fonte': 'PNCP',
                'nome': 'Portal Nacional de Contratações Públicas',
                'url': url_pncp,
                'confianca': 'Alta',
                'tipo': 'API Oficial'
            })
    except Exception as e:
        print(f"Erro PNCP: {e}")
    
    # Busca 2: Google Custom Search (simulado - necessita API key)
    # resultados.extend(buscar_google(objeto, orgao))
    
    # Busca 3: Bing/DDG como fallback
    try:
        url_bing = buscar_bing(f"{orgao} {objeto} edital site:gov.br")
        if url_bing:
            resultados.append({
                'fonte': 'Busca Web',
                'nome': 'Resultado de Busca',
                'url': url_bing,
                'confianca': 'Média',
                'tipo': 'HTML'
            })
    except:
        pass
    
    return resultados

def buscar_pncp(objeto, orgao, data_pub=None):
    """Busca no Portal Nacional de Contratações Públicas"""
    termo_busca = f"{orgao[:50]} {objeto[:100]}"
    
    # Simulação de URL de busca (em produção, usar API real)
    url_busca = f"https://pncp.gov.br/app/editais?q={requests.utils.quote(termo_busca)}"
    
    # Aqui você implementaria a chamada real à API do PNCP
    # Por enquanto retorna URL de busca
    return url_busca

def buscar_bing(query):
    """Busca alternativa via scraping (respeitando robots.txt)"""
    # Implementação simplificada - em produção usar API oficial
    return None

# ============================================================================
# ANÁLISE ESTRUTURADA DO EDITAL
# ============================================================================

def analisar_edital(texto_edital):
    """
    Extrai informações estruturadas do texto do edital
    Retorna dicionário organizado por categorias
    """
    analise = {
        'cabecalho': extrair_cabecalho(texto_edital),
        'objeto': extrair_objeto_detalhado(texto_edital),
        'regras': extrair_regras(texto_edital),
        'prazos': extrair_prazos(texto_edital),
        'valores': extrair_valores(texto_edital),
        'habilitacao': extrair_habilitacao(texto_edital),
        'penalidades': extrair_penalidades(texto_edital),
        'alertas': []
    }
    
    # Gera alertas baseados na análise
    analise['alertas'] = gerar_alertas(analise)
    
    return analise

def extrair_cabecalho(texto):
    """Extrai informações do cabeçalho do edital"""
    info = {}
    
    # Padrões comuns de numeração
    padroes = {
        'numero_edital': r'Edital\s+(?:de\s+Licitacao\s+)?[Nn]?[º°]?\s*(\d{1,6}/\d{4})',
        'numero_processo': r'Processo\s+[Nn]?[º°]?\s*(\d{1,6}/\d{4})',
        'modalidade': r'Modalidade:\s*([^\n]+)',
        'tipo': r'Tipo:\s*([^\n]+)',
        'orgao': r'(?:Orgao|Administracao|Entidade)[:\s]+([^\n]+)',
        'uasg': r'UASG[:\s]+(\d{6})'
    }
    
    for campo, padrao in padroes.items():
        match = re.search(padrao, texto, re.IGNORECASE)
        info[campo] = match.group(1).strip() if match else 'Não identificado'
    
    return info

def extrair_objeto_detalhado(texto):
    """Extrai descrição detalhada do objeto"""
    objeto = {}
    
    # Busca seção do objeto
    padrao_objeto = r'(?:OBJETO|Objeto da Contratacao)[:\s]+(.*?)(?=CAPITULO|CL[AÁ]USULA|\n\n|\Z)'
    match = re.search(padrao_objeto, texto, re.DOTALL | re.IGNORECASE)
    
    if match:
        descricao = match.group(1).strip()
        objeto['descricao_completa'] = descricao[:2000]  # Limita tamanho
        
        # Extrai quantidades
        qtds = re.findall(r'(\d+(?:,\d+)?)\s*(unidades?|metros?|kg|litros?|servicos?)', descricao, re.IGNORECASE)
        objeto['quantidades'] = [f"{q[0]} {q[1]}" for q in qtds[:5]]  # Top 5
        
        # Extrai itens numerados
        itens = re.findall(r'Item\s+\d+[:\s]+([^\n]+)', descricao, re.IGNORECASE)
        objeto['itens_principais'] = itens[:10]  # Top 10
    else:
        objeto['descricao_completa'] = 'Não localizada no edital'
    
    return objeto

def extrair_regras(texto):
    """Extrai regras e critérios de julgamento"""
    regras = {
        'criterio_julgamento': 'Não identificado',
        'tipo_licitacao': 'Não identificado',
        'sistema_preco': 'Não identificado',
        'desconto_maximo': None,
        'lances_minimos': None,
        'empate': 'Não identificado'
    }
    
    # Critério de julgamento
    if re.search(r'menor\s+preco|menor\s+valor', texto, re.IGNORECASE):
        regras['criterio_julgamento'] = 'MENOR PREÇO'
        regras['tipo_licitacao'] = 'Melhor Técnica ou Menor Preço'
    elif re.search(r'maior\s+desconto|desconto\s+sobre', texto, re.IGNORECASE):
        regras['criterio_julgamento'] = 'MAIOR DESCONTO'
        regras['tipo_licitacao'] = 'Concorrência por Maior Desconto'
    elif re.search(r'tecnica\s+e\s+preco|tecnica\s+e\s+valor', texto, re.IGNORECASE):
        regras['criterio_julgamento'] = 'TÉCNICA E PREÇO'
        regras['tipo_licitacao'] = 'Melhor Técnica e Preço'
    
    # Sistema de preço
    if re.search(r'preco\s+global|lote\s+unico', texto, re.IGNORECASE):
        regras['sistema_preco'] = 'PREÇO GLOBAL (Lote Único)'
    elif re.search(r'preco\s+unitario|por\s+item', texto, re.IGNORECASE):
        regras['sistema_preco'] = 'PREÇO UNITÁRIO (Por Item)'
    
    # Limites de desconto
    match_desc = re.search(r'desconto\s+maximo\s+de\s+(\d+)%', texto, re.IGNORECASE)
    if match_desc:
        regras['desconto_maximo'] = int(match_desc.group(1))
    
    return regras

def extrair_prazos(texto):
    """Extrai todas as datas e prazos críticos"""
    prazos = {}
    hoje = datetime.now()
    
    # Padrões de data
    padroes_data = [
        r'(\d{2}/\d{2}/\d{4})',  # DD/MM/AAAA
        r'(\d{2})[./](\d{2})[./](\d{4})',  # Variantes
    ]
    
    # Data de abertura
    match_abertura = re.search(r'Abertura[:\s]+(\d{2}/\d{2}/\d{4})[,\s]+(?:as\s+)?(\d{2})[h:](\d{2})', texto, re.IGNORECASE)
    if match_abertura:
        data_str = match_abertura.group(1)
        try:
            data_abertura = datetime.strptime(data_str, '%d/%m/%Y')
            prazos['data_abertura'] = data_str
            prazos['hora_abertura'] = f"{match_abertura.group(2)}:{match_abertura.group(3)}"
            prazos['dias_restantes'] = (data_abertura - hoje).days
        except:
            pass
    
    # Prazo de entrega da proposta
    match_entrega = re.search(r'entrega\s+(?:das\s+)?propostas?[:\s]+(\d{2}/\d{2}/\d{4})', texto, re.IGNORECASE)
    if match_entrega:
        prazos['entrega_proposta'] = match_entrega.group(1)
    
    # Prazo de vigência da proposta
    match_vigencia = re.search(r'vigencia\s+(?:das\s+)?propostas?[:\s]+(\d+)\s*dias', texto, re.IGNORECASE)
    if match_vigencia:
        prazos['vigencia_proposta_dias'] = int(match_vigencia.group(1))
    
    # Prazo de execução do contrato
    match_execucao = re.search(r'prazo\s+de\s+execucao[:\s]+(\d+)\s*(dias|meses|anos?)', texto, re.IGNORECASE)
    if match_execucao:
        prazos['execucao_contrato'] = f"{match_execucao.group(1)} {match_execucao.group(2)}"
    
    # Validade da proposta
    match_validade = re.search(r'validade\s+(?:da\s+)?proposta[:\s]+(\d+)\s*dias', texto, re.IGNORECASE)
    if match_validade:
        prazos['validade_proposta'] = int(match_validade.group(1))
    
    return prazos

def extrair_valores(texto):
    """Extrai informações financeiras detalhadas"""
    valores = {}
    
    # Valor estimado total
    match_total = re.search(r'valor\s+(?:total\s+)?estimado[:\s]+R?\$?\s*([\d.,]+)', texto, re.IGNORECASE)
    if match_total:
        valores['total_estimado'] = parse_valor(match_total.group(1))
    
    # Valor máximo/mínimo
    match_max = re.search(r'valor\s+maximo[:\s]+R?\$?\s*([\d.,]+)', texto, re.IGNORECASE)
    if match_max:
        valores['maximo'] = parse_valor(match_max.group(1))
    
    # Garantia exigida
    match_garantia = re.search(r'garantia\s+(?:de\s+)?(?:execucao|contratual)?[:\s]+(\d+)%', texto, re.IGNORECASE)
    if match_garantia:
        valores['garantia_percentual'] = int(match_garantia.group(1))
    
    # Índice de reajuste
    match_reajuste = re.search(r'reajuste[:\s]+([^\n]+)', texto, re.IGNORECASE)
    if match_reajuste:
        valores['criterio_reajuste'] = match_reajuste.group(1).strip()
    
    return valores

def extrair_habilitacao(texto):
    """Extrai requisitos de habilitação"""
    hab = {
        'nivel': 'Não identificado',
        'certidoes': [],
        'qualificacao_tecnica': [],
        'qualificacao_economica': [],
        'documentos_obrigatorios': []
    }
    
    # Nível de exigência
    if re.search(r'licitacao\s+plena', texto, re.IGNORECASE):
        hab['nivel'] = 'LICITAÇÃO PLENA (Exigência Total)'
    elif re.search(r'dispensa|inexigibilidade', texto, re.IGNORECASE):
        hab['nivel'] = 'DISPENSA/INEXIGIBILIDADE (Exigência Reduzida)'
    
    # Certidões exigidas
    certidoes_padrao = [
        'federal', 'estadual', 'municipal', 'trabalhistas', 
        'fgts', 'inss', 'cnd', 'regularidade fiscal'
    ]
    for cert in certidoes_padrao:
        if re.search(rf'{cert}', texto, re.IGNORECASE):
            hab['certidoes'].append(cert.upper())
    
    # Qualificação técnica
    if re.search(r'experiencia\s+(\d+)\s+anos', texto, re.IGNORECASE):
        match_exp = re.search(r'experiencia\s+(\d+)\s+anos', texto, re.IGNORECASE)
        hab['qualificacao_tecnica'].append(f"{match_exp.group(1)} anos de experiência")
    
    if re.search(r'registro\s+no\s+crea|cft', texto, re.IGNORECASE):
        hab['qualificacao_tecnica'].append('Registro profissional (CREA/CFT)')
    
    return hab

def extrair_penalidades(texto):
    """Extrai multas e penalidades"""
    penal = {
        'multa_atraso': None,
        'multa_inexecucao': None,
        'garantia_fiel_cumprimento': None,
        'retencao': None
    }
    
    match_multa = re.search(r'multa\s+de\s+(\d+)%', texto, re.IGNORECASE)
    if match_multa:
        penal['multa_atraso'] = f"{match_multa.group(1)}%"
    
    match_inexec = re.search(r'inexecucao.*?(\d+)%', texto, re.IGNORECASE)
    if match_inexec:
        penal['multa_inexecucao'] = f"{match_inexec.group(1)}%"
    
    return penal

def gerar_alertas(analise):
    """Gera alertas de risco baseados na análise"""
    alertas = []
    
    # Alerta de prazo curto
    if analise['prazos'].get('dias_restantes'):
        dias = analise['prazos']['dias_restantes']
        if dias < 3:
            alertas.append({
                'tipo': 'CRÍTICO',
                'cor': 'vermelho',
                'msg': f'Prazo extremamente curto: {dias} dias para entrega!'
            })
        elif dias < 7:
            alertas.append({
                'tipo': 'ATENÇÃO',
                'cor': 'laranja',
                'msg': f'Prazo curto: {dias} dias restantes'
            })
    
    # Alerta de critério de desconto
    if analise['regras']['criterio_julgamento'] == 'MAIOR DESCONTO':
        alertas.append({
            'tipo': 'ESTRATÉGIA',
            'cor': 'azul',
            'msg': 'Concorrência por MAIOR DESCONTO - requer análise de custos detalhada'
        })
    
    # Alerta de garantia alta
    if analise['valores'].get('garantia_percentual'):
        if analise['valores']['garantia_percentual'] > 10:
            alertas.append({
                'tipo': 'FINANCEIRO',
                'cor': 'amarelo',
                'msg': f'Garantia elevada: {analise["valores"]["garantia_percentual"]}%'
            })
    
    # Alerta de habilitação complexa
    if len(analise['habilitacao']['certidoes']) > 5:
        alertas.append({
            'tipo': 'BUROCRATICO',
            'cor': 'cinza',
            'msg': 'Habilitação complexa - iniciar preparação imediata'
        })
    
    return alertas

def parse_valor(valor_str):
    """Converte string de valor para float"""
    try:
        # Remove R$ e espaços
        valor_limpo = valor_str.replace('R$', '').replace(' ', '').strip()
        # Ajusta separadores
        if ',' in valor_limpo and '.' in valor_limpo:
            # Formato brasileiro: 1.234,56
            if valor_limpo.rfind(',') > valor_limpo.rfind('.'):
                valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
            else:
                valor_limpo = valor_limpo.replace(',', '')
        elif ',' in valor_limpo:
            valor_limpo = valor_limpo.replace(',', '.')
        
        return float(valor_limpo)
    except:
        return 0.0

# ============================================================================
# FUNÇÃO PRINCIPAL PARA INTEGRAÇÃO COM APP.PY
# ============================================================================

def obter_analise_completa(licitacao_id, db_path):
    """
    Função principal chamada pela rota /precificar
    Retorna dicionário completo com análise do edital
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Busca dados básicos
    cursor.execute("""
        SELECT orgao, objeto, valor, data_publicacao, url_edital, 
               valor_fechamento, vencedor, status
        FROM licitacoes 
        WHERE id = ?
    """, (licitacao_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    dados_basicos = {
        'id': licitacao_id,
        'orgao': row[0],
        'objeto': row[1],
        'valor_estimado': float(row[2]) if row[2] else 0,
        'data_publicacao': row[3],
        'url_edital_salvo': row[4],
        'valor_fechamento': float(row[5]) if row[5] else None,
        'vencedor': row[6],
        'status': row[7]
    }
    
    # Busca edital original (se não tiver URL salva)
    if not dados_basicos['url_edital_salvo']:
        fontes = buscar_edital_original(
            dados_basicos['objeto'], 
            dados_basicos['orgao'],
            dados_basicos['data_publicacao']
        )
        dados_basicos['fontes_edital'] = fontes
    else:
        dados_basicos['fontes_edital'] = [{
            'fonte': 'Banco Local',
            'url': dados_basicos['url_edital_salvo'],
            'confianca': 'Alta'
        }]
    
    # Se tiver texto do edital (futuro: OCR ou download), analisa
    # Por enquanto, retorna estrutura vazia para preenchimento manual
    dados_basicos['analise_estruturada'] = {
        'status': 'Aguardando download do edital',
        'campos': [
            'cabecalho', 'objeto_detalhado', 'regras', 
            'prazos', 'valores', 'habilitacao', 'penalidades'
        ]
    }
    
    return dados_basicos

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == '__main__':
    # Teste com dados fictícios
    texto_teste = """
    Edital de Licitação nº 45/2024
    Processo: 123/2024
    
    OBJETO: Contratação de empresa para prestação de serviços de engenharia
    
    CRITÉRIO DE JULGAMENTO: Menor preço
    
    ABERTURA: 15/04/2024 às 10:00 horas
    
    VALOR ESTIMADO: R$ 500.000,00
    
    GARANTIA: 5% do valor contratado
    
    PRAZO DE EXECUÇÃO: 180 dias
    
    HABILITAÇÃO: 
    - Certidões negativas federal, estadual e municipal
    - Regularidade do FGTS
    - Experiência mínima de 3 anos
    """
    
    resultado = analisar_edital(texto_teste)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))