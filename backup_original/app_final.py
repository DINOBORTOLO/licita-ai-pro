#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APP.PY - SISTEMA FINAL v3.2
Funcionalidades: Templates externos + Fallback + APIs + Precificação
"""

from flask import Flask, render_template, render_template_string, jsonify, request
import sqlite3
import os
import sys
from datetime import datetime
import traceback

# ==================== CONFIGURAÇÃO ====================

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'banco.db')

# Verifica se banco existe
print(f"📁 Diretório base: {BASE_DIR}")
print(f"🗄️  Banco de dados: {DB_PATH}")
print(f"   Existe: {os.path.exists(DB_PATH)}")

# ==================== TEMPLATES EMBUTIDOS (FALLBACK) ====================

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Robô de Licitações - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { 
            background: rgba(255,255,255,0.95); 
            padding: 30px; 
            border-radius: 15px; 
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header h1 { color: #667eea; margin-bottom: 10px; font-size: 2em; }
        .header p { color: #666; font-size: 1.1em; }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-box { 
            background: rgba(255,255,255,0.95); 
            padding: 25px; 
            border-radius: 12px; 
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .stat-box:hover { transform: translateY(-5px); }
        .stat-number { 
            font-size: 2.5em; 
            font-weight: bold; 
            color: #667eea; 
            margin-bottom: 5px;
        }
        .stat-label { color: #666; font-size: 0.9em; text-transform: uppercase; }
        .content { 
            background: rgba(255,255,255,0.95); 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .content h2 { color: #333; margin-bottom: 20px; }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px;
            font-size: 0.95em;
        }
        th { 
            background: #667eea; 
            color: white; 
            padding: 15px; 
            text-align: left;
            font-weight: 600;
        }
        td { 
            padding: 15px; 
            border-bottom: 1px solid #eee; 
            color: #333;
        }
        tr:hover { background: #f8f9ff; }
        .valor { 
            color: #27ae60; 
            font-weight: bold; 
            font-size: 1.1em;
        }
        .badge { 
            background: #667eea; 
            color: white; 
            padding: 5px 12px; 
            border-radius: 20px; 
            font-size: 0.75em;
            font-weight: 600;
        }
        .btn { 
            background: #667eea; 
            color: white; 
            padding: 8px 16px; 
            text-decoration: none; 
            border-radius: 6px; 
            display: inline-block; 
            margin: 2px;
            font-size: 0.85em;
            transition: all 0.3s;
        }
        .btn:hover { 
            background: #764ba2; 
            transform: scale(1.05);
        }
        .btn-success { background: #27ae60; }
        .btn-success:hover { background: #219a52; }
        .empty-state { 
            text-align: center; 
            padding: 60px 20px; 
            color: #666;
        }
        .empty-state h3 { color: #667eea; margin-bottom: 15px; font-size: 1.5em; }
        .debug-info { 
            margin-top: 30px; 
            padding: 15px; 
            background: #2c3e50; 
            color: #ecf0f1; 
            border-radius: 8px; 
            font-family: 'Courier New', monospace; 
            font-size: 0.85em;
        }
        .oportunidade-alta { border-left: 4px solid #27ae60; background: #f0fff4; }
        .oportunidade-media { border-left: 4px solid #f39c12; background: #fffbf0; }
        .oportunidade-baixa { border-left: 4px solid #e74c3c; background: #fff0f0; }
        @media (max-width: 768px) {
            .stats { grid-template-columns: 1fr 1fr; }
            table { font-size: 0.85em; }
            td, th { padding: 10px; }
            .btn { padding: 6px 10px; font-size: 0.8em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Robô de Licitações Nacional</h1>
            <p>Sistema de Captura e Análise • {{ agora }}</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{{ stats.total }}</div>
                <div class="stat-label">Total Capturado</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{{ stats.hoje }}</div>
                <div class="stat-label">Hoje</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">R$ {{ "%.1f"|format(stats.valor_total/1000000) }}M</div>
                <div class="stat-label">Valor Total</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{{ licitacoes|length }}</div>
                <div class="stat-label">Oportunidades</div>
            </div>
        </div>

        <div class="content">
            <h2>📋 Licitações Encontradas</h2>

            {% if licitacoes %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Órgão</th>
                        <th>Objeto</th>
                        <th>Valor Estimado</th>
                        <th>Data</th>
                        <th>Status</th>
                        <th width="200">Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for lic in licitacoes %}
                    <tr class="{% if lic.valor > 500000 %}oportunidade-alta{% elif lic.valor > 100000 %}oportunidade-media{% else %}oportunidade-baixa{% endif %}">
                        <td><strong>#{{ lic.id }}</strong></td>
                        <td>{{ lic.orgao[:45] if lic.orgao else '-' }}</td>
                        <td>{{ lic.objeto[:60] if lic.objeto else '-' }}</td>
                        <td class="valor">R$ {{ "%.2f"|format(lic.valor|float) }}</td>
                        <td>{{ lic.data_publicacao[:10] if lic.data_publicacao else '-' }}</td>
                        <td><span class="badge">{{ lic.status or 'nova' }}</span></td>
                        <td>
                            <a href="/precificar/{{ lic.id }}" class="btn btn-success">💰 Precificar</a>
                            <a href="/api/licitacao/{{ lic.id }}" class="btn" target="_blank">📄 JSON</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                <h3>Nenhuma licitação encontrada</h3>
                <p>O banco de dados está vazio ou a tabela não existe.</p>
                <p>Execute o coletor: <code>python robo.py</code></p>
            </div>
            {% endif %}

            {% if debug %}
            <div class="debug-info">
                <strong>🔧 Informações de Debug:</strong><br>
                Colunas detectadas: {{ colunas|join(', ') }}<br>
                Modo de renderização: {{ modo }}<br>
                Status do banco: {{ db_status }}<br>
                Timestamp: {{ agora }}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

PRECIFICAR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Precificação - Licitação #{{ lic.id }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .card {
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        .edital-info { 
            background: #f8f9ff; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        .valor-display { 
            font-size: 2em; 
            color: #27ae60; 
            font-weight: bold;
            margin: 10px 0;
        }
        .cenarios {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .cenario {
            background: white;
            border: 2px solid #e0e0e0;
            padding: 25px;
            border-radius: 12px;
            transition: all 0.3s;
            position: relative;
        }
        .cenario:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .cenario.recomendado { 
            border-color: #27ae60; 
            background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
        }
        .cenario.recomendado::before {
            content: "⭐ RECOMENDADO";
            position: absolute;
            top: -12px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: bold;
        }
        .cenario h3 { 
            color: #333; 
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .metric { 
            text-align: center; 
            padding: 15px;
            background: #f8f9ff;
            border-radius: 8px;
            margin: 10px 0;
        }
        .metric-value { 
            font-size: 1.6em; 
            font-weight: bold; 
            color: #667eea; 
        }
        .metric-label { 
            color: #666; 
            font-size: 0.85em;
            margin-top: 5px;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            margin-top: 20px;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #764ba2;
            transform: scale(1.05);
        }
        .btn-outline {
            background: transparent;
            border: 2px solid #667eea;
            color: #667eea;
        }
        .btn-outline:hover {
            background: #667eea;
            color: white;
        }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .alert-info {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>💰 Precificação Inteligente</h1>
            <div class="edital-info">
                <h3>{{ lic.objeto[:100] if lic.objeto else 'Sem descrição' }}</h3>
                <p><strong>Órgão:</strong> {{ lic.orgao }}</p>
                <p><strong>Valor Estimado:</strong> <span class="valor-display">R$ {{ "%.2f"|format(lic.valor|float) }}</span></p>
                <p><strong>ID:</strong> #{{ lic.id }} | <strong>Fonte:</strong> {{ lic.fonte }}</p>
            </div>
        </div>

        <div class="card">
            <h2>📊 Cenários de Lance</h2>
            <div class="alert alert-info">
                💡 <strong>Dica:</strong> O cenário de 25% de desconto oferece o melhor equilíbrio entre competitividade e margem de lucro.
            </div>

            <div class="cenarios">
                <div class="cenario">
                    <h3>Conservador (15%)</h3>
                    <div class="metric">
                        <div class="metric-value">R$ {{ "%.2f"|format(lic.valor * 0.85) }}</div>
                        <div class="metric-label">Preço Proposta</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" style="color: #f39c12;">R$ {{ "%.2f"|format(lic.valor * 0.15) }}</div>
                        <div class="metric-label">Lucro Estimado</div>
                    </div>
                    <p style="text-align: center; margin-top: 15px;">
                        <strong>Chance de Vitória:</strong> ~30%
                    </p>
                </div>

                <div class="cenario recomendado">
                    <h3>Otimizado (25%)</h3>
                    <div class="metric">
                        <div class="metric-value" style="color: #27ae60;">R$ {{ "%.2f"|format(lic.valor * 0.75) }}</div>
                        <div class="metric-label">Preço Proposta</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" style="color: #27ae60;">R$ {{ "%.2f"|format(lic.valor * 0.25) }}</div>
                        <div class="metric-label">Lucro Estimado</div>
                    </div>
                    <p style="text-align: center; margin-top: 15px;">
                        <strong>Chance de Vitória:</strong> ~65%
                    </p>
                </div>

                <div class="cenario">
                    <h3>Agressivo (35%)</h3>
                    <div class="metric">
                        <div class="metric-value" style="color: #e74c3c;">R$ {{ "%.2f"|format(lic.valor * 0.65) }}</div>
                        <div class="metric-label">Preço Proposta</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" style="color: #27ae60;">R$ {{ "%.2f"|format(lic.valor * 0.35) }}</div>
                        <div class="metric-label">Lucro Estimado</div>
                    </div>
                    <p style="text-align: center; margin-top: 15px;">
                        <strong>Chance de Vitória:</strong> ~85%
                    </p>
                </div>
            </div>
        </div>

        <div class="card">
            <a href="/" class="btn">← Voltar ao Dashboard</a>
            <a href="/api/licitacao/{{ lic.id }}" class="btn btn-outline" target="_blank">📄 Ver JSON</a>
        </div>
    </div>
</body>
</html>
"""

# ==================== FUNÇÕES AUXILIARES ====================

def get_db():
    """Retorna conexão com o banco"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def normalizar_licitacao(row):
    """Normaliza uma linha do banco para formato padrão"""
    if not row:
        return None

    # Se é sqlite3.Row, converte para dict
    if hasattr(row, 'keys'):
        data = dict(row)
    else:
        data = row

    # Normaliza campos (tenta várias variações)
    resultado = {
        'id': data.get('id', 0),
        'orgao': data.get('orgao') or data.get('razao_social') or data.get('entidade') or 'Não informado',
        'objeto': data.get('objeto') or data.get('descricao') or data.get('titulo') or 'Sem descrição',
        'valor': float(data.get('valor') or data.get('valor_estimado') or data.get('preco') or 0),
        'data_publicacao': data.get('data_publicacao') or data.get('data') or data.get('data_captura') or '-',
        'status': data.get('status') or data.get('situacao') or 'nova',
        'modalidade': data.get('modalidade') or 'Pregão Eletrônico',
        'fonte': data.get('fonte') or 'N/A',
        'numero_controle': data.get('numero_controle') or '',
        'link': data.get('link') or '#'
    }

    return resultado

def get_colunas():
    """Retorna lista de colunas da tabela"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(licitacoes)")
        colunas = [row[1] for row in cursor.fetchall()]
        conn.close()
        return colunas
    except:
        return []

def get_estatisticas():
    """Retorna estatísticas do banco"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Total
        cursor.execute("SELECT COUNT(*) FROM licitacoes")
        total = cursor.fetchone()[0]

        # Hoje
        cursor.execute("SELECT COUNT(*) FROM licitacoes WHERE date(data_captura) = date('now')")
        hoje = cursor.fetchone()[0]

        # Valor total
        cursor.execute("SELECT SUM(valor) FROM licitacoes")
        valor_total = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total': total,
            'hoje': hoje,
            'valor_total': float(valor_total)
        }
    except:
        return {'total': 0, 'hoje': 0, 'valor_total': 0}

# ==================== ROTAS ====================

@app.route('/')
def dashboard():
    """Dashboard principal"""
    try:
        # Estatísticas
        stats = get_estatisticas()

        # Busca licitações
        colunas = get_colunas()
        licitacoes = []

        if colunas:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM licitacoes ORDER BY id DESC LIMIT 100")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                lic = normalizar_licitacao(row)
                if lic:
                    licitacoes.append(lic)

        # Decide modo de renderização
        modo = "Template Embutido (Fallback)"
        try:
            # Tenta template externo primeiro
            return render_template('dashboard.html', 
                                 stats=stats,
                                 licitacoes=licitacoes,
                                 agora=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        except:
            # Usa template embutido
            modo = "Template Embutido (Fallback)"

        return render_template_string(DASHBOARD_TEMPLATE,
                                    stats=stats,
                                    licitacoes=licitacoes,
                                    colunas=colunas,
                                    debug=True,
                                    modo=modo,
                                    db_status="OK" if colunas else "Sem tabela",
                                    agora=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    except Exception as e:
        erro_detalhado = traceback.format_exc()
        return f"""
        <h1>❌ Erro no Dashboard</h1>
        <div style="background: #ffebee; padding: 20px; border-radius: 10px; margin: 20px;">
            <p><strong>Erro:</strong> {str(e)}</p>
            <pre style="background: #333; color: #0f0; padding: 15px; overflow-x: auto;">{erro_detalhado}</pre>
        </div>
        <a href="/" style="margin: 20px;">🔄 Tentar novamente</a>
        """, 500

@app.route('/precificar/<int:licitacao_id>')
def precificar(licitacao_id):
    """Página de precificação"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM licitacoes WHERE id = ?", (licitacao_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return """
            <h1>❌ Licitação não encontrada</h1>
            <p>O ID solicitado não existe no banco de dados.</p>
            <a href="/">← Voltar ao Dashboard</a>
            """, 404

        lic = normalizar_licitacao(row)

        # Tenta template externo
        try:
            return render_template('precificador.html', lic=lic)
        except:
            pass

        # Usa template embutido
        return render_template_string(PRECIFICAR_TEMPLATE, lic=lic)

    except Exception as e:
        return f"""
        <h1>❌ Erro na Precificação</h1>
        <p>{str(e)}</p>
        <pre>{traceback.format_exc()}</pre>
        <a href="/">← Voltar</a>
        """, 500

@app.route('/api/licitacoes')
def api_licitacoes():
    """API - Lista todas as licitações"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Verifica se tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='licitacoes'")
        if not cursor.fetchone():
            return jsonify({
                'status': 'erro',
                'mensagem': 'Tabela licitacoes não existe'
            }), 404

        cursor.execute("SELECT * FROM licitacoes ORDER BY id DESC LIMIT 100")
        rows = cursor.fetchall()
        conn.close()

        licitacoes = [normalizar_licitacao(row) for row in rows]

        return jsonify({
            'status': 'ok',
            'quantidade': len(licitacoes),
            'timestamp': datetime.now().isoformat(),
            'licitacoes': licitacoes
        })

    except Exception as e:
        return jsonify({
            'status': 'erro',
            'mensagem': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/licitacao/<int:id>')
def api_licitacao_detalhe(id):
    """API - Detalhes de uma licitação"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM licitacoes WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({
                'status': 'erro',
                'mensagem': f'Licitação {id} não encontrada'
            }), 404

        lic = normalizar_licitacao(row)

        # Adiciona análise de precificação
        valor = lic['valor']
        lic['analise_precificacao'] = {
            'cenario_conservador': {
                'desconto': '15%',
                'preco_proposta': round(valor * 0.85, 2),
                'lucro_estimado': round(valor * 0.15, 2),
                'chance_vitoria': '30%'
            },
            'cenario_recomendado': {
                'desconto': '25%',
                'preco_proposta': round(valor * 0.75, 2),
                'lucro_estimado': round(valor * 0.25, 2),
                'chance_vitoria': '65%'
            },
            'cenario_agressivo': {
                'desconto': '35%',
                'preco_proposta': round(valor * 0.65, 2),
                'lucro_estimado': round(valor * 0.35, 2),
                'chance_vitoria': '85%'
            }
        }

        return jsonify({
            'status': 'ok',
            'licitacao': lic
        })

    except Exception as e:
        return jsonify({
            'status': 'erro',
            'mensagem': str(e)
        }), 500

@app.route('/api/saude')
def saude():
    """API - Health check"""
    return jsonify({
        'status': 'ok',
        'servidor': 'online',
        'banco_existe': os.path.exists(DB_PATH),
        'colunas': get_colunas(),
        'timestamp': datetime.now().isoformat()
    })

# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🤖 ROBÔ DE LICITAÇÕES - SISTEMA FINAL v3.2")
    print("="*70)
    print("  ✅ Funcionalidades:")
    print("     • Dashboard com estatísticas")
    print("     • Precificação inteligente (3 cenários)")
    print("     • APIs REST completas")
    print("     • Templates externos + Fallback embutido")
    print("     • Detecção automática de colunas")
    print("="*70)
    print(f"  🌐 Acesse: http://localhost:5000")
    print(f"  🔧 Debug:  http://localhost:5000/api/saude")
    print(f"  📊 API:    http://localhost:5000/api/licitacoes")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)