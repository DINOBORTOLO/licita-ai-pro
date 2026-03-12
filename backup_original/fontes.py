"""
FONTES DE LICITAÇÕES - VERSÃO FINAL
Extrai dados reais com links para embed no sistema
"""

import requests
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict

def extrair_valor(valor_str):
    """Extrai valor numérico de qualquer formato"""
    if isinstance(valor_str, (int, float)):
        return float(valor_str)
    
    valor_str = str(valor_str)
    # Remove tudo exceto números, ponto e vírgula
    valor_limpo = re.sub(r'[^\d.,]', '', valor_str)
    
    try:
        # Detecta formato brasileiro vs americano
        if ',' in valor_limpo and '.' in valor_limpo:
            if valor_limpo.rfind(',') > valor_limpo.rfind('.'):
                valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
            else:
                valor_limpo = valor_limpo.replace(',', '')
        elif ',' in valor_limpo:
            valor_limpo = valor_limpo.replace(',', '.')
        
        return float(valor_limpo) if valor_limpo else 0.0
    except:
        return 0.0

def buscar_pncp(pagina=1):
    """
    Busca no PNCP com número de controle para embed
    """
    url = "https://pncp.gov.br/api/search/"
    
    params = {
        "q": "*",
        "page": pagina,
        "pageSize": 50,
        "sort": "date",
        "order": "desc"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://pncp.gov.br/'
    }
    
    try:
        print(f"  🔍 PNCP página {pagina}...")
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            print(f"  ⚠️ PNCP status {resp.status_code}")
            return []
        
        dados = resp.json()
        licitacoes = []
        
        for item in dados.get("items", []):
            numero_controle = item.get("numeroControle", "")
            sequencial = item.get("sequencial", "")
            
            # LINK PARA EMBED NO SISTEMA (não redireciona)
            if numero_controle:
                # Link direto do PNCP que permite embed
                link_embed = f"https://pncp.gov.br/comprasPublicas/{numero_controle}"
                tipo_link = "embed"
            else:
                # Fallback: busca no portal
                objeto_busca = item.get("objeto", "")[:30].replace(" ", "%20")
                link_embed = f"https://pncp.gov.br/app/editais?q={objeto_busca}"
                tipo_link = "busca"
            
            licitacao = {
                "orgao": item.get("orgaoNome", "Não informado"),
                "objeto": item.get("objeto", ""),
                "valor": extrair_valor(item.get("valorTotal") or item.get("valorEstimado", 0)),
                "data_publicacao": item.get("dataPublicacao", ""),
                "link": link_embed,
                "fonte": "PNCP",
                "modalidade": item.get("modalidade", ""),
                "situacao": item.get("situacao", ""),
                "numero_controle": numero_controle,
                "sequencial": sequencial,
                "tipo_link": tipo_link
            }
            licitacoes.append(licitacao)
        
        print(f"  ✅ PNCP: {len(licitacoes)} licitações")
        return licitacoes
        
    except Exception as e:
        print(f"  ❌ Erro PNCP: {str(e)[:80]}")
        return []

def buscar_comprasgov(pagina=1):
    """
    Busca no Compras.gov.br
    """
    url = "https://compras.dados.gov.br/licitacoes/v1/licitacoes.json"
    
    params = {
        "offset": (pagina - 1) * 100,
        "order": "desc"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    try:
        print(f"  🔍 ComprasGov...")
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            return []
        
        dados = resp.json()
        licitacoes = []
        
        for item in dados.get("_embedded", {}).get("licitacoes", []):
            # Extrai ID da URL
            self_link = item.get("_links", {}).get("self", {}).get("href", "")
            licitacao_id = self_link.split("/")[-1] if self_link else ""
            
            # Link para embed no ComprasGov
            if licitacao_id:
                link_embed = f"https://compras.gov.br/legislacao/pregao-electronico/{licitacao_id}"
                tipo_link = "embed"
            else:
                objeto = item.get("objeto", "")[:30].replace(" ", "+")
                link_embed = f"https://compras.gov.br/consulta/editais?q={objeto}"
                tipo_link = "busca"
            
            licitacao = {
                "orgao": item.get("orgao", {}).get("nome", "Não informado"),
                "objeto": item.get("objeto", ""),
                "valor": extrair_valor(item.get("valor", 0)),
                "data_publicacao": item.get("publicacao", ""),
                "link": link_embed,
                "fonte": "COMPRASGOV",
                "modalidade": item.get("modalidade", ""),
                "situacao": item.get("situacao", ""),
                "numero_controle": licitacao_id,
                "sequencial": None,
                "tipo_link": tipo_link
            }
            licitacoes.append(licitacao)
        
        print(f"  ✅ ComprasGov: {len(licitacoes)} licitações")
        return licitacoes
        
    except Exception as e:
        print(f"  ❌ Erro ComprasGov: {str(e)[:80]}")
        return []

def buscar_todas_fontes():
    """
    Coleta de todas as fontes
    """
    todas = []
    
    print("\n" + "="*60)
    print("🔍 COLETA DE LICITAÇÕES")
    print("="*60)
    
    # PNCP (2 páginas)
    p1 = buscar_pncp(1)
    todas.extend(p1)
    if len(p1) > 0:
        todas.extend(buscar_pncp(2))
    
    # ComprasGov
    todas.extend(buscar_comprasgov(1))
    
    print(f"\n{'='*60}")
    print(f"📊 TOTAL: {len(todas)} licitações")
    print(f"{'='*60}")
    
    # Mostra exemplo
    if todas:
        print(f"\n🔗 Exemplo de link gerado:")
        ex = todas[0]
        print(f"   Fonte: {ex['fonte']}")
        print(f"   Número: {ex['numero_controle'] or 'N/A'}")
        print(f"   Tipo: {ex['tipo_link']}")
        print(f"   Link: {ex['link'][:60]}...")
    
    return todas