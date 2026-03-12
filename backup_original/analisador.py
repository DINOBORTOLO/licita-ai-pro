"""
ANALISADOR FINANCEIRO
Calcula custos, margens e viabilidade de licitações
"""

def custo_estimado(valor, tipo="produto"):
    """
    Estima custo baseado no tipo de produto/serviço
    """
    fatores = {
        "produto": 0.65,      # 35% margem
        "servico": 0.55,      # 45% margem
        "obra": 0.70,         # 30% margem
        "material_construcao": 0.60,
        "informatica": 0.75,
        "limpeza": 0.55,
        "escolar": 0.60
    }
    
    fator = fatores.get(tipo, 0.65)
    return valor * fator

def margem(valor, custo=None):
    """
    Calcula margem de lucro
    Se custo não informado, estima automaticamente
    """
    if custo is None:
        custo = custo_estimado(valor)
    
    if valor <= 0:
        return 0.0
    
    lucro = valor - custo
    return lucro / valor

def calcular_lucro(valor_estimado, tipo="produto"):
    """
    Calcula lucro estimado completo
    """
    custo = custo_estimado(valor_estimado, tipo)
    lucro = valor_estimado - custo
    margem_pct = (lucro / valor_estimado) if valor_estimado > 0 else 0
    
    return {
        "valor_estimado": valor_estimado,
        "custo_estimado": custo,
        "lucro_estimado": lucro,
        "margem": margem_pct,
        "margem_percentual": f"{margem_pct * 100:.1f}%"
    }

def analisar_edital(texto_objeto, valor_estimado):
    """
    Análise completa de edital (versão básica sem IA)
    """
    # Detecta tipo pelo texto
    texto_lower = texto_objeto.lower()
    
    if any(p in texto_lower for p in ["servico", "execucao", "instalacao"]):
        tipo = "servico"
    elif any(p in texto_lower for p in ["obra", "construcao", "reforma"]):
        tipo = "obra"
    elif any(p in texto_lower for p in ["material construcao", "cimento", "tijolo"]):
        tipo = "material_construcao"
    elif any(p in texto_lower for p in ["computador", "notebook", "impressora"]):
        tipo = "informatica"
    elif any(p in texto_lower for p in ["limpeza", "detergente", "papel"]):
        tipo = "limpeza"
    elif any(p in texto_lower for p in ["escolar", "cadeira escolar", "uniforme"]):
        tipo = "escolar"
    else:
        tipo = "produto"
    
    # Calcula financeiro
    financeiro = calcular_lucro(valor_estimado, tipo)
    
    # Análise de viabilidade simples
    margem_val = financeiro["margem"]
    
    if margem_val >= 0.35:
        viabilidade = 75
        recomendacao = "EXCELENTE"
        chance = "70%"
    elif margem_val >= 0.30:
        viabilidade = 60
        recomendacao = "BOA"
        chance = "55%"
    elif margem_val >= 0.25:
        viabilidade = 50
        recomendacao = "REGULAR"
        chance = "45%"
    else:
        viabilidade = 35
        recomendacao = "AVALIAR"
        chance = "30%"
    
    # Preço sugerido (para 30% de margem)
    preco_sugerido = valor_estimado * 0.70
    
    return {
        "viabilidade": viabilidade,
        "recomendacao": recomendacao,
        "preco_sugerido": preco_sugerido,
        "margem_recomendada": "30%",
        "chance_vitoria": chance,
        "custo_estimado": financeiro["custo_estimado"],
        "lucro_estimado": financeiro["lucro_estimado"],
        "margem_calculada": financeiro["margem_percentual"],
        "tipo_detectado": tipo,
        "riscos": ["Concorrência desconhecida", "Prazo a verificar"],
        "exigencias": ["Certidões negativas", "Regularidade fiscal"],
        "documentos": ["CNPJ", "Contrato Social", "Certidão Federal"]
    }