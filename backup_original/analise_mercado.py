import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple
from datetime import datetime
import io
import base64
from dataclasses import dataclass

@dataclass
class AnaliseMercado:
    objeto: str
    preco_edital: float
    estatisticas: Dict
    historico: List[Dict]
    recomendacao: str
    risco: str
    grafico_base64: str

class AnalisadorMercado:
    def __init__(self):
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def gerar_analise_completa(self, objeto: str, preco_edital: float, 
                               historico: List[Dict]) -> AnaliseMercado:
        """Gera análise completa de mercado com visualizações"""
        
        from banco import calcular_estatisticas_historico
        stats = calcular_estatisticas_historico(historico)
        
        # Gerar gráfico comparativo
        grafico = self._gerar_grafico_comparativo(historico, preco_edital, stats)
        
        # Análise de risco baseada na dispersão histórica
        risco = self._avaliar_risco(stats, preco_edital)
        
        # Recomendação estratégica
        recomendacao = self._gerar_recomendacao(stats, preco_edital, risco)
        
        return AnaliseMercado(
            objeto=objeto,
            preco_edital=preco_edital,
            estatisticas=stats,
            historico=historico,
            recomendacao=recomendacao,
            risco=risco,
            grafico_base64=grafico
        )
    
    def _gerar_grafico_comparativo(self, historico: List[Dict], 
                                   preco_edital: float, stats: Dict) -> str:
        """Gera gráfico de comparação histórica em base64"""
        
        df = pd.DataFrame(historico)
        if df.empty:
            return ""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Gráfico 1: Evolução temporal de preços
        df['data'] = pd.to_datetime(df['data_homologacao'])
        df = df.sort_values('data')
        
        ax1.plot(df['data'], df['valor_estimado'], 'o-', label='Valor Edital', 
                color='#e74c3c', linewidth=2, markersize=8)
        ax1.plot(df['data'], df['valor_vencedor'], 's-', label='Valor Vencedor', 
                color='#27ae60', linewidth=2, markersize=8)
        ax1.axhline(y=preco_edital, color='#3498db', linestyle='--', 
                   label='Seu Edital Atual', linewidth=2)
        
        ax1.fill_between(df['data'], df['valor_vencedor'], df['valor_estimado'], 
                        alpha=0.3, color='gray', label='Margem de Negociação')
        
        ax1.set_title('Histórico de Preços - Últimas Licitações', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Data da Licitação')
        ax1.set_ylabel('Valor (R$)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Formatar eixo Y como moeda
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'R${x:,.0f}'.replace(',', '.')))
        
        # Gráfico 2: Boxplot de dispersão de preços vencedores
        precos_vencedores = df['valor_vencedor'].tolist()
        precos_vencedores.append(stats['preco_sugerido'])  # Incluir sugestão atual
        
        bp = ax2.boxplot([precos_vencedores], labels=['Preços Vencedores\nHistóricos'],
                        patch_artist=True, widths=0.6)
        bp['boxes'][0].set_facecolor('#3498db')
        bp['boxes'][0].set_alpha(0.7)
        
        # Destacar preço sugerido
        ax2.scatter([1], [stats['preco_sugerido']], color='red', s=200, 
                   marker='*', label='Sugestão Atual', zorder=5)
        ax2.axhline(y=preco_edital, color='orange', linestyle='--', 
                   label='Valor Edital Atual', linewidth=2)
        
        ax2.set_title('Distribuição dos Preços Vencedores', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Valor (R$)')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'R${x:,.0f}'.replace(',', '.')))
        
        plt.tight_layout()
        
        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        imagem_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return imagem_base64
    
    def _avaliar_risco(self, stats: Dict, preco_edital: float) -> str:
        """Avalia o risco da operação baseado na volatilidade histórica"""
        
        if stats['qtd_amostras'] < 3:
            return "ALTO"  # Poucos dados históricos
        
        desvio_relativo = (stats['desvio_padrao'] / stats['media_vencedor']) * 100
        
        if desvio_relativo < 5:
            return "BAIXO"
        elif desvio_relativo < 15:
            return "MÉDIO"
        else:
            return "ALTO"
    
    def _gerar_recomendacao(self, stats: Dict, preco_edital: float, risco: str) -> str:
        """Gera texto de recomendação estratégica"""
        
        desconto_necessario = ((preco_edital - stats['preco_sugerido']) / preco_edital) * 100
        
        if stats['qtd_amostras'] == 0:
            return "Sem dados históricos. Use margem de segurança de 20-25%."
        
        texto = f"""
        <strong>Análise de {stats['qtd_amostras']} licitações similares:</strong><br>
        • Desconto médio de mercado: <strong>{stats['desconto_medio']:.1f}%</strong><br>
        • Faixa de descontos históricos: {stats['desconto_min']:.1f}% a {stats['desconto_max']:.1f}%<br>
        • Preço mínimo já registrado: R$ {stats['preco_minimo']:,.2f}<br><br>
        
        <strong>Para este edital (R$ {preco_edital:,.2f}):</strong><br>
        • Desconto necessário para vitória: <strong>{desconto_necessario:.1f}%</strong><br>
        • Preço sugerido: <strong>R$ {stats['preco_sugerido']:,.2f}</strong><br>
        • Faixa recomendada: R$ {stats['faixa_recomendada_min']:,.2f} a R$ {stats['faixa_recomendada_max']:,.2f}<br><br>
        
        <strong>Estratégia:</strong> {'Oferte próximo à mediana histórica' if desconto_necessario <= stats['desconto_medio'] else 'Edital com margem apertada. Considere custos operacionais cuidadosamente.'}
        """
        
        return texto
    
    def simular_cenario(self, preco_edital: float, stats: Dict, 
                        margem_desejada: float) -> Dict:
        """Simula diferentes cenários de preço"""
        
        preco_ofertado = preco_edital * (1 - (margem_desejada / 100))
        prob_vitoria = self._calcular_probabilidade_vitoria(preco_ofertado, stats)
        
        return {
            'margem_desejada': margem_desejada,
            'preco_ofertado': preco_ofertado,
            'lucro_potencial': preco_ofertado * (margem_desejada / 100),
            'probabilidade_vitoria': prob_vitoria,
            'retorno_esperado': (preco_ofertado * (margem_desejada / 100)) * (prob_vitoria / 100)
        }
    
    def _calcular_probabilidade_vitoria(self, preco_ofertado: float, stats: Dict) -> float:
        """Estima probabilidade de vitória baseada na distribuição histórica"""
        
        if stats['qtd_amostras'] < 3:
            return 50.0  # Incerteza máxima
        
        # Se oferta for menor que mínimo histórico, alta chance
        if preco_ofertado <= stats['preco_minimo']:
            return 85.0
        
        # Se for maior que máximo, baixa chance
        if preco_ofertado >= stats['preco_maximo']:
            return 15.0
        
        # Interpolação linear simples
        faixa = stats['preco_maximo'] - stats['preco_minimo']
        posicao = stats['preco_maximo'] - preco_ofertado
        
        return 15 + (posicao / faixa) * 70  # 15% a 85%
    
    def gerar_relatorio_pdf(self, analise: AnaliseMercado) -> str:
        """Gera relatório em formato texto estruturado (simulando PDF)"""
        
        relatorio = f"""
        RELATÓRIO DE ANÁLISE DE MERCADO - ROBÔ DE LICITAÇÕES
        Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        
        OBJETO: {analise.objeto}
        VALOR ESTIMADO DO EDITAL: R$ {analise.preco_edital:,.2f}
        
        1. RESUMO ESTATÍSTICO
        Licitações analisadas: {analise.estatisticas['qtd_amostras']}
        Preço médio vencedor histórico: R$ {analise.estatisticas['media_vencedor']:,.2f}
        Desconto médio de mercado: {analise.estatisticas['desconto_medio']:.1f}%
        Desvio padrão: R$ {analise.estatisticas['desvio_padrao']:,.2f}
        
        2. RECOMENDAÇÃO DE PREÇO
        Preço sugerido: R$ {analise.estatisticas['preco_sugerido']:,.2f}
        Faixa recomendada: R$ {analise.estatisticas['faixa_recomendada_min']:,.2f} a R$ {analise.estatisticas['faixa_recomendada_max']:,.2f}
        Nível de confiança: {analise.estatisticas['confianca']:.0f}%
        
        3. AVALIAÇÃO DE RISCO: {analise.risco}
        
        4. ESTRATÉGIA RECOMENDADA
        {analise.recomendacao}
        
        5. HISTÓRICO DETALHADO
        """
        
        for i, lic in enumerate(analise.historico[:5], 1):
            relatorio += f"""
        {i}. {lic['orgao']} ({lic['data_homologacao']})
           Edital: R$ {lic['valor_estimado']:,.2f} | Vencedor: R$ {lic['valor_vencedor']:,.2f}
           Desconto: {lic['desconto_percentual']:.1f}%
        """
        
        return relatorio
