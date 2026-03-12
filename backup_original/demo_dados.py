"""
Dados de demonstração para testar o sistema
Quando as APIs do governo estiverem fora do ar
"""

import random
from datetime import datetime, timedelta

ORGAOS = [
    "Prefeitura Municipal de São Paulo",
    "Prefeitura de Belo Horizonte",
    "Governo do Estado de MG",
    "Prefeitura de Curitiba",
    "Universidade Federal de Minas Gerais",
    "Hospital das Clínicas de Porto Alegre",
    "Prefeitura de Recife",
    "Secretaria de Educação do RJ",
    "Prefeitura de Brasília",
    "Instituto Federal de SP"
]

OBJETOS = [
    "Aquisição de 500 cadeiras escolares para rede municipal de ensino",
    "Fornecimento de material escolar completo - kit aluno",
    "Contratação de serviços de reforma de escolas estaduais",
    "Aquisição de equipamentos para cozinha industrial",
    "Fornecimento de uniformes escolares - 2.000 unidades",
    "Instalação de cobertura metálica em quadra poliesportiva",
    "Aquisição de notebooks para professores - 300 unidades",
    "Fornecimento de material de limpeza hospitalar",
    "Construção de escola modular em estrutura metálica",
    "Reforma e ampliação de unidade de saúde",
    "Aquisição de playground e equipamentos recreativos",
    "Fornecimento de cimento e material de construção",
    "Instalação de energia solar em prédios públicos",
    "Aquisição de fogão industrial e freezer para merenda escolar",
    "Contratação de serviços de manutenção predial"
]

def gerar_licitacoes_demo(quantidade=15):
    """Gera licitações fictícias para demonstração"""
    licitacoes = []
    
    for i in range(quantidade):
        orgao = random.choice(ORGAOS)
        objeto = random.choice(OBJETOS)
        
        # Valor entre 50 mil e 5 milhões
        valor = random.randint(50000, 5000000)
        
        # Data aleatória nos últimos 7 dias
        dias_atras = random.randint(0, 7)
        data = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        
        licitacao = {
            "orgao": orgao,
            "objeto": objeto,
            "valor": valor,
            "data_publicacao": data,
            "link": f"https://pncp.gov.br/demo/{i}",
            "fonte": random.choice(["PNCP", "COMPRASGOV"]),
            "modalidade": "Pregão Eletrônico",
            "situacao": "Aberta"
        }
        licitacoes.append(licitacao)
    
    return licitacoes

def buscar_todas_fontes_demo():
    """Versão de demonstração do buscador"""
    print("\n🎮 MODO DEMONSTRAÇÃO ATIVADO")
    print("Gerando licitações de teste para você visualizar o sistema...\n")
    
    licitacoes = gerar_licitacoes_demo(20)
    print(f"✓ {len(licitacoes)} licitações de demonstração geradas")
    return licitacoes