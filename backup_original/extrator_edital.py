
"""
EXTRATOR DE EDITAIS
Busca, baixa e processa editais dos portais oficiais
Mantém tudo no sistema sem redirecionar cliente
"""

import requests
import re
import json
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass
import os

@dataclass
class EditalCompleto:
    """Estrutura completa de um edital"""
    id: str
    orgao: str
    objeto: str
    valor_estimado: float
    data_abertura: Optional[str]
    data_publicacao: str
    modalidade: str
    situacao: str
    
    # Conteúdo
    texto_completo: str
    anexos: List[Dict]
    link_original: str
    
    # Processado
    resumo_ia: Optional[str] = None
    exigencias: List[str] = None
    documentos_necessarios: List[str] = None
    prazo_execucao: Optional[int] = None
    garantia: Optional[float] = None
    
    # Arquivos locais
    pdf_local: Optional[str] = None
    html_local: Optional[str] = None


class ExtratorEdital:
    """
    Extrai conteúdo completo de editais dos portais oficiais
    """
    
    def __init__(self, pasta_cache: str = "editais_cache"):
        self.pasta_cache = pasta_cache
        os.makedirs(pasta_cache, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extrair_pncp(self, numero_controle: str) -> Optional[EditalCompleto]:
        """
        Extrai edital completo do PNCP
        """
        try:
            # API de detalhes do PNCP
            url_api = f"https://pncp.gov.br/api/compras/{numero_controle}"
            
            print(f"  🔍 Buscando edital {numero_controle} no PNCP...")
            resp = self.session.get(url_api, timeout=30)
            
            if resp.status_code != 200:
                print(f"  ⚠️ API retornou {resp.status_code}")
                return self._extrair_pncp_scraping(numero_controle)
            
            dados = resp.json()
            
            # Extrai texto do edital
            texto_edital = self._extrair_texto_edital(dados)
            
            # Busca anexos/PDFs
            anexos = self._buscar_anexos_pncp(numero_controle)
            
            # Baixa PDF se existir
            pdf_path = None
            if anexos:
                pdf_path = self._baixar_anexo(anexos[0], numero_controle)
            
            edital = EditalCompleto(
                id=numero_controle,
                orgao=dados.get("orgaoEntidade", {}).get("razaoSocial", ""),
                objeto=dados.get("objetoCompra", ""),
                valor_estimado=float(dados.get("valorTotalEstimado", 0) or 0),
                data_abertura=dados.get("dataAberturaProposta"),
                data_publicacao=dados.get("dataPublicacaoPncp", ""),
                modalidade=dados.get("modalidadeNome", ""),
                situacao=dados.get("situacaoCompra", ""),
                texto_completo=texto_edital,
                anexos=anexos,
                link_original=f"https://pncp.gov.br/comprasPublicas/{numero_controle}",
                pdf_local=pdf_path
            )
            
            # Salva cache
            self._salvar_cache(edital)
            
            return edital
            
        except Exception as e:
            print(f"  ❌ Erro ao extrair: {e}")
            return None
    
    def _extrair_pncp_scraping(self, numero_controle: str) -> Optional[EditalCompleto]:
        """
        Fallback: extrai via scraping se API falhar
        """
        url = f"https://pncp.gov.br/comprasPublicas/{numero_controle}"
        
        try:
            resp = self.session.get(url, timeout=30)
            if resp.status_code != 200:
                return None
            
            html = resp.text
            
            # Extrai dados do HTML
            orgao = self._extrair_meta(html, 'orgao') or "Não informado"
            objeto = self._extrair_meta(html, 'objeto') or "Não informado"
            valor = self._extrair_valor_html(html)
            
            # Extrai texto do edital do HTML
            texto = self._limpar_html(html)
            
            return EditalCompleto(
                id=numero_controle,
                orgao=orgao,
                objeto=objeto,
                valor_estimado=valor,
                data_abertura=None,
                data_publicacao=datetime.now().isoformat(),
                modalidade="Pregão Eletrônico",
                situacao="Aberto",
                texto_completo=texto[:5000],  # Primeiros 5000 chars
                anexos=[],
                link_original=url
            )
            
        except Exception as e:
            print(f"  ❌ Scraping falhou: {e}")
            return None
    
    def _extrair_texto_edital(self, dados: Dict) -> str:
        """Extrai texto completo do edital"""
        partes = []
        
        # Objeto
        partes.append(f"OBJETO: {dados.get('objetoCompra', '')}")
        
        # Descrição detalhada se existir
        if 'descricao' in dados:
            partes.append(f"\nDESCRIÇÃO:\n{dados['descricao']}")
        
        # Itens da licitação
        itens = dados.get('itens', [])
        if itens:
            partes.append("\nITENS:")
            for i, item in enumerate(itens[:20], 1):  # Limita 20 itens
                partes.append(f"  {i}. {item.get('descricao', '')} - Qtd: {item.get('quantidade', 0)}")
        
        # Critérios de julgamento
        criterios = dados.get('criterioJulgamentoNome', '')
        if criterios:
            partes.append(f"\nCRITÉRIO DE JULGAMENTO: {criterios}")
        
        # Condições de pagamento
        pagamento = dados.get('condicaoPagamento', '')
        if pagamento:
            partes.append(f"\nCONDIÇÃO DE PAGAMENTO: {pagamento}")
        
        # Prazos
        entrega = dados.get('prazoEntrega', '')
        if entrega:
            partes.append(f"\nPRAZO DE ENTREGA: {entrega}")
        
        return "\n".join(partes)
    
    def _buscar_anexos_pncp(self, numero_controle: str) -> List[Dict]:
        """Busca documentos anexos do edital"""
        # Endpoint de anexos do PNCP
        url = f"https://pncp.gov.br/api/compras/{numero_controle}/anexos"
        
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json().get("anexos", [])
        except:
            pass
        
        return []
    
    def _baixar_anexo(self, anexo: Dict, edital_id: str) -> Optional[str]:
        """Baixa PDF do anexo e salva localmente"""
        url = anexo.get("url") or anexo.get("link")
        if not url:
            return None
        
        nome_arquivo = f"{edital_id}_{anexo.get('nome', 'edital')}.pdf"
        caminho = os.path.join(self.pasta_cache, nome_arquivo)
        
        # Se já existe, retorna cache
        if os.path.exists(caminho):
            return caminho
        
        try:
            print(f"  📥 Baixando PDF...")
            resp = self.session.get(url, timeout=60, stream=True)
            
            if resp.status_code == 200:
                with open(caminho, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  ✅ PDF salvo: {caminho}")
                return caminho
        except Exception as e:
            print(f"  ⚠️ Erro ao baixar PDF: {e}")
        
        return None
    
    def _salvar_cache(self, edital: EditalCompleto):
        """Salva edital em cache JSON"""
        cache_file = os.path.join(self.pasta_cache, f"{edital.id}.json")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                'id': edital.id,
                'orgao': edital.orgao,
                'objeto': edital.objeto,
                'valor_estimado': edital.valor_estimado,
                'data_abertura': edital.data_abertura,
                'data_publicacao': edital.data_publicacao,
                'modalidade': edital.modalidade,
                'situacao': edital.situacao,
                'texto_completo': edital.texto_completo[:10000],  # Limita tamanho
                'link_original': edital.link_original,
                'pdf_local': edital.pdf_local,
                'cache_em': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def _extrair_meta(self, html: str, campo: str) -> Optional[str]:
        """Extrai metadados do HTML"""
        padrao = rf'<meta[^>]*name=["\']{campo}["\'][^>]*content=["\']([^"\']+)["\']'
        match = re.search(padrao, html, re.I)
        if match:
            return match.group(1)
        
        # Tenta regex alternativo
        padrao2 = rf'{campo}["\']?\s*[:=]\s*["\']?([^"\'<>]+)'
        match = re.search(padrao2, html, re.I)
        return match.group(1) if match else None
    
    def _extrair_valor_html(self, html: str) -> float:
        """Extrai valor estimado do HTML"""
        padroes = [
            r'valor\s*(?:total|estimado)?\s*[:=]?\s*R?\$?\s*([\d.,]+)',
            r'R\$\s*([\d.,]+)\s*(?:reais)?',
            r'([\d.,]+)\s*(?:mil|milhões?|bilhões?)\s*(?:de)?\s*reais'
        ]
        
        for padrao in padroes:
            match = re.search(padrao, html, re.I)
            if match:
                valor_str = match.group(1).replace('.', '').replace(',', '.')
                try:
                    return float(valor_str)
                except:
                    continue
        
        return 0.0
    
    def _limpar_html(self, html: str) -> str:
        """Remove tags HTML e extrai texto limpo"""
        # Remove scripts e styles
        html = re.sub(r'<(script|style)[^>]*>[^<]*</\1>', '', html, flags=re.I)
        # Remove tags
        texto = re.sub(r'<[^>]+>', ' ', html)
        # Remove espaços excessivos
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()


# Instância global
extrator = ExtratorEdital()

def obter_edital_completo(numero_controle: str, fonte: str = "PNCP") -> Optional[EditalCompleto]:
    """
    Função principal para obter edital completo
    """
    if fonte.upper() == "PNCP":
        return extrator.extrair_pncp(numero_controle)
    
    # Adicionar outras fontes aqui
    return None