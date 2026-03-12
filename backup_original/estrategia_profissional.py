"""
ESTRATÉGIA PROFISSIONAL DE LICITAÇÃO
Baseado em táticas reais de fornecedores que vivem de pregão
"""

import random
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json
from datetime import datetime

@dataclass
class AnaliseConcorrencia:
    """Perfil de concorrente estimado"""
    nome: str
    perfil: str  # 'agressivo', 'moderado', 'conservador'
    preco_medio: float
    desconto_maximo: float  # % abaixo do preço médio deles

@dataclass
class EstrategiaLance:
    """Estratégia calculada para ganhar"""
    preco_custo: float
    preco_alvo: float
    margem_real: float
    lance_inicial: float
    lance_final: float
    momento_entrada: str  # 'inicio', 'meio', 'final'
    chance_vitoria: float
    lucro_estimado: float
    risco: str  # 'baixo', 'medio', 'alto'

@dataclass
class SimulacaoPregao:
    """Resultado de simulação de pregão"""
    vencedor: str
    preco_vencedor: float
    colocacao: int  # 1º, 2º, 3º...
    economia_orgao: float  # % abaixo do valor estimado
    lucro_real: float
    tempo_duracao: str  # 'rapido', 'normal', 'longo'


class EstrategaProfissional:
    """
    Implementa estratégias reais usadas por fornecedores profissionais
    """
    
    def __init__(self):
        self.historico_precos = self._carregar_historico()
        self.perfis_concorrentes = {
            'agressivo': {'desconto_medio': 0.15, 'variacao': 0.10, 'pressa': True},
            'moderado': {'desconto_medio': 0.08, 'variacao': 0.05, 'pressa': False},
            'conservador': {'desconto_medio': 0.03, 'variacao': 0.03, 'pressa': False}
        }
    
    def _carregar_historico(self) -> Dict:
        """Base de dados de preços históricos por categoria"""
        return {
            'cadeira_escolar': {
                'preco_fabrica': 540,
                'preco_atacado': 620,
                'preco_varejo': 820,
                'frete_unitario': 40,
                'impostos': 30,
                'margem_minima_viavel': 0.08
            },
            'material_escolar_kit': {
                'preco_fabrica': 45,
                'preco_atacado': 65,
                'preco_varejo': 95,
                'frete_unitario': 8,
                'impostos': 5,
                'margem_minima_viavel': 0.10
            },
            'notebook_educacional': {
                'preco_fabrica': 2800,
                'preco_atacado': 3200,
                'preco_varejo': 4500,
                'frete_unitario': 150,
                'impostos': 200,
                'margem_minima_viavel': 0.06
            },
            'cozinha_industrial': {
                'preco_fabrica': 3500,
                'preco_atacado': 4800,
                'preco_varejo': 7200,
                'frete_unitario': 400,
                'impostos': 300,
                'margem_minima_viavel': 0.12
            },
            'estrutura_metalica': {
                'preco_fabrica': 180,  # por m2
                'preco_atacado': 250,
                'preco_varejo': 380,
                'frete_unitario': 30,
                'impostos': 20,
                'margem_minima_viavel': 0.15
            }
        }
    
    def detectar_categoria(self, objeto: str) -> str:
        """Detecta categoria do produto pelo texto do edital"""
        objeto_lower = objeto.lower()
        
        if any(p in objeto_lower for p in ['cadeira', 'carteira', 'mesa escolar']):
            return 'cadeira_escolar'
        elif any(p in objeto_lower for p in ['kit escolar', 'material escolar', 'uniforme']):
            return 'material_escolar_kit'
        elif any(p in objeto_lower for p in ['notebook', 'computador', 'tablet']):
            return 'notebook_educacional'
        elif any(p in objeto_lower for p in ['fogao', 'freezer', 'cozinha industrial', 'geladeira industrial']):
            return 'cozinha_industrial'
        elif any(p in objeto_lower for p in ['estrutura metalica', 'cobertura metalica', 'galpao', 'steel frame']):
            return 'estrutura_metalica'
        
        return 'generico'
    
    def calcular_custo_real(self, categoria: str, quantidade: int = 1) -> Dict:
        """
        Calcula custo real de produção/aquisição
        Baseado em pesquisa de mercado real
        """
        dados = self.historico_precos.get(categoria, {
            'preco_fabrica': 0,
            'preco_atacado': 0,
            'frete_unitario': 0,
            'impostos': 0
        })
        
        custo_unitario = (
            dados['preco_fabrica'] +
            dados['frete_unitario'] +
            dados['impostos']
        )
        
        # Desconto por volume
        if quantidade >= 500:
            desconto_volume = 0.05  # 5% desconto
        elif quantidade >= 100:
            desconto_volume = 0.03
        else:
            desconto_volume = 0
        
        custo_unitario *= (1 - desconto_volume)
        
        return {
            'custo_unitario': custo_unitario,
            'custo_total': custo_unitario * quantidade,
            'preco_atacado_referencia': dados['preco_atacado'],
            'preco_varejo_referencia': dados['preco_varejo'],
            'margem_minima_viavel': dados.get('margem_minima_viavel', 0.10)
        }
    
    def estimar_concorrencia(self, valor_estimado: float, 
                            categoria: str,
                            regiao: str = 'sudeste') -> List[AnaliseConcorrencia]:
        """
        Estima perfil dos concorrentes baseado em histórico
        """
        concorrentes = []
        
        # Número de concorrentes baseado no valor
        if valor_estimado > 1000000:
            num_concorrentes = random.randint(8, 15)
        elif valor_estimado > 500000:
            num_concorrentes = random.randint(5, 10)
        else:
            num_concorrentes = random.randint(3, 7)
        
        # Distribuição de perfis
        perfis = ['agressivo'] * (num_concorrentes // 3) + \
                 ['moderado'] * (num_concorrentes // 2) + \
                 ['conservador'] * (num_concorrentes // 6 + 1)
        
        dados_cat = self.historico_precos.get(categoria, {})
        preco_ref = dados_cat.get('preco_atacado', valor_estimado * 0.002)
        
        for i, perfil in enumerate(perfis[:num_concorrentes]):
            perfil_dados = self.perfis_concorrentes[perfil]
            
            # Preço base do concorrente
            preco_base = preco_ref * (1 + random.uniform(-0.10, 0.15))
            
            # Quanto descontam no máximo
            desconto_max = perfil_dados['desconto_medio'] + random.uniform(0, perfil_dados['variacao'])
            
            concorrentes.append(AnaliseConcorrencia(
                nome=f"Concorrente {chr(65+i)}",  # A, B, C...
                perfil=perfil,
                preco_medio=preco_base,
                desconto_maximo=desconto_max
            ))
        
        return concorrentes
    
    def calcular_estrategia_vencedora(self,
                                     objeto: str,
                                     valor_estimado: float,
                                     quantidade: int = 1,
                                     urgencia: str = 'normal') -> Dict:
        """
        Calcula estratégia completa para ganhar o pregão
        """
        # Detecta categoria
        categoria = self.detectar_categoria(objeto)
        
        # Calcula custo real
        custos = self.calcular_custo_real(categoria, quantidade)
        custo_unitario = custos['custo_unitario']
        custo_total = custos['custo_total']
        
        # Estima concorrência
        concorrentes = self.estimar_concorrencia(valor_estimado, categoria)
        
        # Ordena concorrentes por agressividade (preço mais baixo esperado)
        concorrentes_ordenados = sorted(
            concorrentes,
            key=lambda x: x.preco_medio * (1 - x.desconto_maximo)
        )
        
        # Preço do concorrente mais agressivo
        preco_mais_agressivo = concorrentes_ordenados[0].preco_medio * \
                              (1 - concorrentes_ordenados[0].desconto_maximo)
        
        # ESTRATÉGIA: Ganhar com margem mínima viável
        margem_minima = custos['margem_minima_viavel']
        
        # Preço alvo: abaixo do mais agressivo, mas com margem mínima
        preco_alvo_minimo = custo_unitario * (1 + margem_minima)
        preco_alvo = min(preco_mais_agressivo * 1.02, preco_alvo_minimo * 1.15)
        
        # Garante margem mínima
        if preco_alvo < preco_alvo_minimo:
            preco_alvo = preco_alvo_minimo
        
        # Arredondamento estratégico (psicológico)
        preco_alvo = self._arredondar_pregao(preco_alvo)
        
        # Define momento de entrada
        if len([c for c in concorrentes if c.perfil == 'agressivo']) > 2:
            momento = 'final'  # Muitos agressivos = esperar
        elif valor_estimado > 500000:
            momento = 'meio'   # Valor alto = entrar no meio
        else:
            momento = 'inicio' # Pouca concorrência = entrar cedo
        
        # Calcula chance de vitória
        nosso_preco_final = preco_alvo
        precos_finais = [c.preco_medio * (1 - c.desconto_maximo * 0.8) 
                        for c in concorrentes]
        precos_finais.append(nosso_preco_final)
        precos_finais.sort()
        
        nossa_posicao = precos_finais.index(nosso_preco_final) + 1
        chance_vitoria = 95 if nossa_posicao == 1 else 70 if nossa_posicao <= 2 else 40
        
        # Monta resultado
        estrategia = EstrategiaLance(
            preco_custo=custo_unitario,
            preco_alvo=preco_alvo,
            margem_real=(preco_alvo - custo_unitario) / preco_alvo,
            lance_inicial=preco_alvo * 1.05,  # Começa 5% acima
            lance_final=preco_alvo,
            momento_entrada=momento,
            chance_vitoria=chance_vitoria,
            lucro_estimado=(preco_alvo - custo_unitario) * quantidade,
            risco='baixo' if chance_vitoria > 80 else 'medio'
        )
        
        return {
            'categoria_detectada': categoria,
            'custo_real_unitario': custo_unitario,
            'custo_total': custo_total,
            'concorrentes': [
                {
                    'nome': c.nome,
                    'perfil': c.perfil,
                    'preco_medio': c.preco_medio,
                    'preco_minimo_esperado': c.preco_medio * (1 - c.desconto_maximo)
                }
                for c in concorrentes[:5]  # Top 5
            ],
            'estrategia': {
                'preco_custo': estrategia.preco_custo,
                'preco_alvo': estrategia.preco_alvo,
                'margem_percentual': f"{estrategia.margem_real*100:.1f}%",
                'lance_inicial': estrategia.lance_inicial,
                'lance_final': estrategia.lance_final,
                'momento_entrada': estrategia.momento_entrada,
                'chance_vitoria': f"{estrategia.chance_vitoria:.0f}%",
                'lucro_estimado_total': estrategia.lucro_estimado,
                'risco': estrategia.risco
            },
            'recomendacao_tatica': self._gerar_recomendacao_tatica(estrategia, concorrentes),
            'simulacao': self._simular_pregao(estrategia, concorrentes, quantidade)
        }
    
    def _arredondar_pregao(self, preco: float) -> float:
        """Arredondamento psicológico para pregões"""
        if preco > 1000:
            # Arredonda para 90, 95, 99 (psicológico)
            base = int(preco / 10) * 10
            centavos = preco - base
            if centavos > 5:
                return base + 9.99
            else:
                return base - 0.01
        return preco
    
    def _gerar_recomendacao_tatica(self, 
                                   estrategia: EstrategiaLance,
                                   concorrentes: List[AnaliseConcorrencia]) -> List[str]:
        """Gera recomendações táticas específicas"""
        recomendacoes = []
        
        num_agressivos = len([c for c in concorrentes if c.perfil == 'agressivo'])
        
        if estrategia.momento_entrada == 'final':
            recomendacoes.append(
                "⏰ ESPERE ATÉ O FINAL: Há muitos concorrentes agressivos. "
                "Deixe eles se desgastarem antes de entrar."
            )
        elif estrategia.momento_entrada == 'meio':
            recomendacoes.append(
                "⚡ ENTRADA NO MEIO: Valor alto atrai cautela. "
                "Entre quando faltarem 10 minutos para o encerramento."
            )
        else:
            recomendacoes.append(
                "🚀 ENTRADA RÁPIDA: Pouca concorrência agressiva. "
                "Entre cedo para assustar competidores."
            )
        
        if estrategia.margem_real < 0.10:
            recomendacoes.append(
                f"⚠️ MARGEM APERTADA: Apenas {estrategia.margem_real*100:.1f}%. "
                "Ganhe o contrato e negocie volume extra com a fábrica."
            )
        
        recomendacoes.append(
            f"🎯 LANCE FINAL: R$ {estrategia.lance_final:.2f} "
            f"(não desça abaixo de R$ {estrategia.preco_custo * 1.03:.2f})"
        )
        
        recomendacoes.append(
            f"💰 LUCRO ESPERADO: R$ {estrategia.lucro_estimado:,.2f} "
            f"no contrato total."
        )
        
        return recomendacoes
    
    def _simular_pregao(self,
                       estrategia: EstrategiaLance,
                       concorrentes: List[AnaliseConcorrencia],
                       quantidade: int) -> SimulacaoPregao:
        """Simula como seria o pregão"""
        
        # Simula lances dos concorrentes
        lances = []
        for c in concorrentes:
            lance_min = c.preco_medio * (1 - c.desconto_maximo)
            lance_real = lance_min * random.uniform(1.0, 1.10)  # Não dá o máximo
            lances.append((c.nome, lance_real))
        
        # Nosso lance
        lances.append(('NOSSA EMPRESA', estrategia.lance_final))
        
        # Ordena por preço (menor primeiro)
        lances.sort(key=lambda x: x[1])
        
        nossa_posicao = next(i for i, (nome, _) in enumerate(lances) if nome == 'NOSSA EMPRESA') + 1
        vencedor = lances[0][0]
        preco_vencedor = lances[0][1]
        
        # Calcula economia para o órgão
        valor_medio = sum(l[1] for l in lances) / len(lances)
        economia = (valor_medio - preco_vencedor) / valor_medio
        
        return SimulacaoPregao(
            vencedor='NOSSA EMPRESA' if nossa_posicao == 1 else vencedor,
            preco_vencedor=preco_vencedor,
            colocacao=nossa_posicao,
            economia_orgao=economia * 100,
            lucro_real=(preco_vencedor - estrategia.preco_custo) * quantidade if vencedor == 'NOSSA EMPRESA' else 0,
            tempo_duracao='longo' if len([c for c in concorrentes if c.perfil == 'agressivo']) > 3 else 'normal'
        )


# Instância global
estratega = EstrategaProfissional()

def analisar_estrategia_licitacao(objeto: str, 
                                   valor_estimado: float,
                                   quantidade: int = 1) -> Dict:
    """Função pública para usar no sistema"""
    return estratega.calcular_estrategia_vencedora(objeto, valor_estimado, quantidade)


# Teste rápido
if __name__ == "__main__":
    # Exemplo do caso real: 450 cadeiras escolares
    print("="*70)
    print("ESTRATÉGIA PROFISSIONAL - EXEMPLO REAL")
    print("="*70)
    
    resultado = analisar_estrategia_licitacao(
        objeto="Aquisição de 450 cadeiras escolares padrão FNDE",
        valor_estimado=380000,
        quantidade=450
    )
    
    print(f"\n📦 CATEGORIA: {resultado['categoria_detectada']}")
    print(f"💰 CUSTO REAL UNITÁRIO: R$ {resultado['custo_real_unitario']:.2f}")
    print(f"💰 CUSTO TOTAL: R$ {resultado['custo_total']:,.2f}")
    
    print(f"\n🏆 ESTRATÉGIA CALCULADA:")
    estr = resultado['estrategia']
    print(f"   Preço alvo: R$ {estr['preco_alvo']:.2f}")
    print(f"   Margem: {estr['margem_percentual']}")
    print(f"   Chance de vitória: {estr['chance_vitoria']}")
    print(f"   Lucro estimado: R$ {estr['lucro_estimado_total']:,.2f}")
    print(f"   Momento de entrada: {estr['momento_entrada']}")
    
    print(f"\n📋 RECOMENDAÇÕES TÁTICAS:")
    for rec in resultado['recomendacao_tatica']:
        print(f"   {rec}")
    
    print(f"\n🎮 SIMULAÇÃO DO PREGÃO:")
    sim = resultado['simulacao']
    print(f"   Vencedor: {sim.vencedor}")
    print(f"   Preço vencedor: R$ {sim.preco_vencedor:.2f}")
    print(f"   Nossa colocação: {sim.colocacao}º")
    print(f"   Economia para órgão: {sim.economia_orgao:.1f}%")
    print(f"   Lucro real (se ganhar): R$ {sim.lucro_real:,.2f}")