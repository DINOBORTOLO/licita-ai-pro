"""
FONTES HÍBRIDO: APIs + Dados de Demonstração
Quando APIs do governo falham, gera dados realistas para teste
"""

import requests
import random
from datetime import datetime, timedelta
from typing import List, Dict

# Dados realistas para demonstração
ORGAOS_DEMO = [
    "Prefeitura Municipal de São Paulo - SP",
    "Prefeitura de Belo Horizonte - MG",
    "Prefeitura de Curitiba - PR",
    "Prefeitura de Recife - PE",
    "Prefeitura de Porto Alegre - RS",
    "Governo do Estado de Minas Gerais",
    "Governo do Estado de São Paulo",
    "Universidade Federal de Minas Gerais",
    "Hospital das Clínicas de Porto Alegre",
    "Secretaria de Educação do Rio de Janeiro",
    "Prefeitura de Brasília - DF",
    "Instituto Federal de São Paulo",
    "Prefeitura de Salvador - BA",
    "Prefeitura de Fortaleza - CE",
    "Prefeitura de Manaus - AM"
]

OBJETOS_DEMO = [
    {"nome": "Aquisição de 500 cadeiras escolares", "categoria": "escolar", "valor_min": 80000, "valor_max": 150000},
    {"nome": "Fornecimento de material escolar completo - kit aluno", "categoria": "escolar", "valor_min": 50000, "valor_max": 300000},
    {"nome": "Contratação de serviços de reforma de escolas", "categoria": "obra", "valor_min": 200000, "valor_max": 2000000},
    {"nome": "Aquisição de equipamentos para cozinha industrial", "categoria": "cozinha", "valor_min": 60000, "valor_max": 400000},
    {"nome": "Fornecimento de uniformes escolares", "categoria": "escolar", "valor_min": 40000, "valor_max": 250000},
    {"nome": "Instalação de cobertura metálica em quadra poliesportiva", "categoria": "obra", "valor_min": 150000, "valor_max": 800000},
    {"nome": "Aquisição de notebooks para professores", "categoria": "informatica", "valor_min": 100000, "valor_max": 600000},
    {"nome": "Fornecimento de material de limpeza hospitalar", "categoria": "limpeza", "valor_min": 30000, "valor_max": 180000},
    {"nome": "Construção de escola modular em estrutura metálica", "categoria": "obra", "valor_min": 500000, "valor_max": 5000000},
    {"nome": "Reforma e ampliação de unidade de saúde", "categoria": "obra", "valor_min": 300000, "valor_max": 3000000},
    {"nome": "Aquisição de playground e equipamentos recreativos", "categoria": "escolar", "valor_min": 45000, "valor_max": 350000},
    {"nome": "Fornecimento de cimento e material de construção", "categoria": "material", "valor_min": 60000, "valor_max": 500000},
    {"nome": "Instalação de energia solar em prédios públicos", "categoria": "obra", "valor_min": 200000, "valor_max": 1500000},
    {"nome": "Aquisição de fogão industrial e freezer", "categoria": "cozinha", "valor_min": 35000, "valor_max": 200000},
    {"nome": "Contratação de serviços de manutenção predial", "categoria": "servico", "valor_min": 50000, "valor_max": 400000},
    {"nome": "Fornecimento de computadores e impressoras", "categoria": "informatica", "valor_min": 80000, "valor_max": 450000},
    {"nome": "Aquisição de equipamentos esportivos", "categoria": "escolar", "valor_min": 25000, "valor_max": 180000},
    {"nome": "Reforma de ginásio poliesportivo", "categoria": "obra", "valor_min": 180000, "valor_max": 1200000},
    {"nome": "Fornecimento de mobiliário de escritório", "categoria": "escritorio", "valor_min": 40000, "valor_max": 300000},
    {"nome": "Aquisição de sistema de segurança e CFTV", "categoria": "informatica", "valor_min": 70000, "valor_max": 500000}
]


def gerar_licitacoes_demo(quantidade=20) -> List[Dict]:
    """
    Gera licitações de demonstração realistas
    COM LINKS DE BUSCA FUNCIONAIS (não links diretos falsos)
    """
    licitacoes = []
    hoje = datetime.now()
    
    for i in range(quantidade):
        # Seleciona objeto aleatório
        obj_template = random.choice(OBJETOS_DEMO)
        
        # Gera valores
        valor = random.randint(obj_template["valor_min"], obj_template["valor_max"])
        
        # Data aleatória (últimos 7 dias)
        dias_atras = random.randint(0, 7)
        data_pub = (hoje - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        
        # LINK DE BUSCA FUNCIONAL (não edital específico falso)
        termo_busca = obj_template["nome"][:25].replace(" ", "%20")
        
        if random.choice([True, False]):
            # Busca no PNCP
            link_funcional = f"https://pncp.gov.br/app/editais?q={termo_busca}"
            fonte = "PNCP"
        else:
            # Busca no ComprasGov
            link_funcional = f"https://compras.gov.br/consulta/editais?q={termo_busca}"
            fonte = "COMPRASGOV"
        
        # Monta objeto completo
        licitacao = {
            "orgao": random.choice(ORGAOS_DEMO),
            "objeto": obj_template["nome"],
            "valor": valor,
            "data_publicacao": data_pub,
            "link": link_funcional,
            "fonte": fonte,
            "modalidade": random.choice(["Pregão Eletrônico", "Concorrência", "Dispensa de Licitação"]),
            "situacao": "Aberto",
            "numero_controle": None,
            "sequencial": None,
            "tipo_link": "busca"
        }
        
        licitacoes.append(licitacao)
    
    return licitacoes


def buscar_pncp_real(pagina=1):
    """Tenta buscar PNCP real"""
    try:
        url = "https://pncp.gov.br/api/search/"
        params = {"q": "*", "page": pagina, "pageSize": 50}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            dados = resp.json()
            licitacoes = []
            
            for item in dados.get("items", []):
                numero = item.get("numeroControle", "")
                licitacoes.append({
                    "orgao": item.get("orgaoNome", "Não informado"),
                    "objeto": item.get("objeto", ""),
                    "valor": float(item.get("valorTotal") or item.get("valorEstimado", 0) or 0),
                    "data_publicacao": item.get("dataPublicacao", ""),
                    "link": f"https://pncp.gov.br/comprasPublicas/{numero}" if numero else "#",
                    "fonte": "PNCP",
                    "modalidade": item.get("modalidade", ""),
                    "situacao": item.get("situacao", ""),
                    "numero_controle": numero,
                    "sequencial": item.get("sequencial", ""),
                    "tipo_link": "embed" if numero else "busca"
                })
            return licitacoes
            
    except Exception as e:
        print(f"    API PNCP falhou: {str(e)[:50]}")
    
    return None


def buscar_comprasgov_real():
    """Tenta buscar ComprasGov real"""
    try:
        url = "https://compras.dados.gov.br/licitacoes/v1/licitacoes.json"
        params = {"offset": 0}
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            dados = resp.json()
            licitacoes = []
            
            for item in dados.get("_embedded", {}).get("licitacoes", []):
                link_self = item.get("_links", {}).get("self", {}).get("href", "")
                lic_id = link_self.split("/")[-1] if link_self else ""
                
                licitacoes.append({
                    "orgao": item.get("orgao", {}).get("nome", "Não informado"),
                    "objeto": item.get("objeto", ""),
                    "valor": float(item.get("valor", 0) or 0),
                    "data_publicacao": item.get("publicacao", ""),
                    "link": f"https://compras.gov.br/legislacao/pregao-electronico/{lic_id}" if lic_id else "#",
                    "fonte": "COMPRASGOV",
                    "modalidade": item.get("modalidade", ""),
                    "situacao": item.get("situacao", ""),
                    "numero_controle": lic_id,
                    "sequencial": None,
                    "tipo_link": "embed" if lic_id else "busca"
                })
            return licitacoes
            
    except Exception as e:
        print(f"    API ComprasGov falhou: {str(e)[:50]}")
    
    return None


def buscar_todas_fontes() -> List[Dict]:
    """
    COLETA HÍBRIDA:
    1. Tenta APIs reais
    2. Se falhar, usa dados de demonstração
    """
    todas = []
    modo_demo = False
    
    print("\n" + "="*60)
    print("🔍 COLETA DE LICITAÇÕES")
    print("="*60)
    
    # Tenta PNCP real
    print("  📡 Tentando PNCP (API real)...")
    pncp_real = buscar_pncp_real(1)
    
    if pncp_real is not None and len(pncp_real) > 0:
        todas.extend(pncp_real)
        print(f"  ✅ PNCP real: {len(pncp_real)} licitações")
    else:
        print("  ⚠️ PNCP indisponível")
        modo_demo = True
    
    # Tenta ComprasGov real
    print("  📡 Tentando ComprasGov (API real)...")
    gov_real = buscar_comprasgov_real()
    
    if gov_real is not None and len(gov_real) > 0:
        todas.extend(gov_real)
        print(f"  ✅ ComprasGov real: {len(gov_real)} licitações")
    else:
        print("  ⚠️ ComprasGov indisponível")
        modo_demo = True
    
    # Se APIs falharam, gera demonstração
    if len(todas) == 0:
        print("\n" + "!"*60)
        print("🎮 MODO DEMONSTRAÇÃO ATIVADO")
        print("   (APIs do governo estão fora do ar)")
        print("!"*60)
        
        licitacoes_demo = gerar_licitacoes_demo(25)
        todas.extend(licitacoes_demo)
        
        print(f"\n  ✅ Geradas {len(licitacoes_demo)} licitações de demonstração")
        print("  💡 Estas são fictícias mas realistas para teste")
    
    # Resumo
    print(f"\n{'='*60}")
    print(f"📊 TOTAL: {len(todas)} licitações")
    if modo_demo:
        print(f"   ⚠️ MODO DEMONSTRAÇÃO (dados de teste)")
    else:
        print(f"   ✅ DADOS REAIS do governo")
    print(f"{'='*60}")
    
    # Mostra exemplo
    if todas:
        print(f"\n🔗 Exemplo:")
        ex = todas[0]
        print(f"   Órgão: {ex['orgao'][:50]}...")
        print(f"   Objeto: {ex['objeto'][:50]}...")
        print(f"   Valor: R$ {ex['valor']:,.2f}")
        print(f"   Link: {ex['link'][:60]}...")
    
    return todas