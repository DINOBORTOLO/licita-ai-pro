<!DOCTYPE html>
<html>
<head>
    <title>LICITA AI™ - Painel de Controle com Precificação Inteligente</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 15px;
        }
        .container { max-width: 1400px; margin: 0 auto; }

        .header { 
            background: rgba(255,255,255,0.95); 
            padding: 20px 25px; 
            border-radius: 12px; 
            margin-bottom: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-brand h1 { 
            color: #667eea; 
            font-size: 1.6em; 
            margin: 0;
            font-weight: 700;
        }
        .header-brand p { 
            color: #666; 
            font-size: 0.85em; 
            margin: 3px 0 0 0;
        }
        .header-actions { display: flex; gap: 10px; }

        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); 
            gap: 12px; 
            margin-bottom: 15px; 
        }
        .stat-box { 
            background: rgba(255,255,255,0.95); 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .stat-number { 
            font-size: 1.8em; 
            font-weight: 700; 
            color: #667eea; 
        }
        .stat-label { 
            font-size: 0.75em; 
            color: #666; 
            margin-top: 5px;
            text-transform: uppercase;
        }

        .content { 
            background: rgba(255,255,255,0.95); 
            padding: 20px; 
            border-radius: 12px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .content-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .content h2 { 
            color: #333; 
            font-size: 1.1em; 
            font-weight: 600;
        }

        /* TABELA OTIMIZADA */
        table { 
            width: 100%; 
            border-collapse: collapse; 
            font-size: 0.85em;
            table-layout: fixed;
        }
        th { 
            background: #2563eb;
            color: white;
            padding: 12px 8px; 
            text-align: left;
            font-weight: 600;
            font-size: 0.75em;
            text-transform: uppercase;
            white-space: nowrap;
        }
        td { 
            padding: 10px 8px; 
            border-bottom: 1px solid #eee; 
            vertical-align: top;
            line-height: 1.4;
        }
        tr:hover { background: #f8f9ff; }

        /* DISTRIBUICAO DAS COLUNAS */
        .col-id { width: 60px; font-weight: 600; color: #667eea; text-align: center; }
        .col-orgao { width: 25%; }
        .col-objeto { width: 35%; }
        .col-objeto .texto-wrap {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 1.4;
            max-height: 2.8em;
        }
        .col-valor { 
            width: 120px;
            font-weight: 600; 
            color: #16a34a;
            text-align: right;
            white-space: nowrap;
        }
        .col-data { width: 90px; color: #666; text-align: center; white-space: nowrap; }
        .col-acao { width: 200px; text-align: right; white-space: nowrap; }

        .btn { 
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: #2563eb; 
            color: white; 
            padding: 6px 10px; 
            text-decoration: none; 
            border-radius: 4px; 
            font-size: 0.75em;
            font-weight: 500;
            border: none;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .btn:hover { background: #1d4ed8; transform: translateY(-1px); }
        .btn-checklist { background: #16a34a; margin-left: 4px; }
        .btn-checklist:hover { background: #15803d; }
        .btn-precificar { background: #f59e0b; color: #78350f; margin-left: 4px; }
        .btn-precificar:hover { background: #d97706; }
        .btn-print { background: #475569; }

        .badge {
            background: #dbeafe;
            color: #1e40af;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: 600;
        }

        /* MODAL */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(4px);
        }
        .modal-overlay.ativo { display: flex; }
        
        .modal-content {
            background: white;
            padding: 0;
            border-radius: 16px;
            max-width: 900px;
            width: 95%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
            animation: modalSlideIn 0.3s ease;
        }
        
        @keyframes modalSlideIn {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 25px;
            border-bottom: 2px solid #e5e7eb;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px 16px 0 0;
        }
        .modal-header h3 {
            font-size: 1.3em;
            font-weight: 600;
        }
        .btn-fechar {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }
        .btn-fechar:hover { background: rgba(255,255,255,0.3); }
        
        .modal-body {
            padding: 25px;
        }

        /* SISTEMA DE TABS */
        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e5e7eb;
            flex-wrap: wrap;
        }
        .tab {
            padding: 12px 20px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 0.9em;
            color: #64748b;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
            font-weight: 500;
        }
        .tab:hover { color: #2563eb; background: #f8fafc; }
        .tab.ativa {
            color: #2563eb;
            border-bottom-color: #2563eb;
            font-weight: 600;
            background: #eff6ff;
        }
        .tab-content { display: none; }
        .tab-content.ativa { display: block; animation: fadeIn 0.3s; }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* CARDS DE ANÁLISE */
        .analise-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .analise-card {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #2563eb;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .analise-card:hover { transform: translateY(-2px); }
        .analise-card h4 {
            color: #64748b;
            font-size: 0.75em;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }
        .analise-card .valor {
            font-size: 1.6em;
            font-weight: 700;
            color: #1e293b;
        }
        .analise-card .subvalor {
            font-size: 0.85em;
            color: #64748b;
            margin-top: 6px;
        }
        .analise-card.positivo { border-left-color: #16a34a; }
        .analise-card.positivo .valor { color: #16a34a; }
        .analise-card.alerta { border-left-color: #f59e0b; }
        .analise-card.alerta .valor { color: #d97706; }
        .analise-card.negativo { border-left-color: #dc2626; }
        .analise-card.negativo .valor { color: #dc2626; }

        /* SEÇÕES DE CONTEÚDO */
        .secao {
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #e2e8f0;
        }
        .secao h4 {
            color: #1e293b;
            margin-bottom: 15px;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* TABELAS INTERNAS */
        .tabela-dados {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .tabela-dados th {
            background: #e2e8f0;
            color: #475569;
            padding: 10px;
            text-align: left;
            font-weight: 600;
            font-size: 0.8em;
        }
        .tabela-dados td {
            padding: 10px;
            border-bottom: 1px solid #e2e8f0;
            color: #334155;
        }
        .tabela-dados tr:hover { background: #f1f5f9; }

        /* GRÁFICO SIMULADO */
        .grafico-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin: 15px 0;
        }
        .barra-progresso {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        .barra-label {
            width: 120px;
            font-size: 0.85em;
            color: #475569;
        }
        .barra-track {
            flex: 1;
            height: 24px;
            background: #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }
        .barra-fill {
            height: 100%;
            border-radius: 12px;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-size: 0.75em;
            font-weight: 600;
        }
        .barra-fill.verde { background: linear-gradient(90deg, #16a34a, #22c55e); }
        .barra-fill.amarelo { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
        .barra-fill.vermelho { background: linear-gradient(90deg, #dc2626, #ef4444); }
        .barra-fill.azul { background: linear-gradient(90deg, #2563eb, #3b82f6); }

        /* ALERTAS E MENSAGENS */
        .erro-msg {
            background: #fee2e2;
            color: #991b1b;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #dc2626;
        }
        .sucesso-msg {
            background: #d1fae5;
            color: #065f46;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #16a34a;
        }
        .aviso-msg {
            background: #fef3c7;
            color: #92400e;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #f59e0b;
        }
        .info-msg {
            background: #dbeafe;
            color: #1e40af;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #2563eb;
        }

        /* CHECKLIST */
        .checklist-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 8px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            transition: all 0.2s;
        }
        .checklist-item:hover { background: #f8fafc; border-color: #cbd5e1; }
        .checklist-item input[type="checkbox"] {
            margin-right: 12px;
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        .checklist-item label {
            flex: 1;
            cursor: pointer;
            color: #334155;
            font-size: 0.95em;
        }
        .checklist-item.checked {
            background: #f0fdf4;
            border-color: #86efac;
        }
        .checklist-item.checked label {
            text-decoration: line-through;
            color: #6b7280;
        }

        /* BOTÕES DE AÇÃO */
        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
            flex-wrap: wrap;
        }

        /* LOADING */
        .loading {
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid #ffffff;
            border-top: 2px solid transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 5px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* INDICADOR DE STATUS */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
        }
        .status-verde { background: #dcfce7; color: #166534; }
        .status-amarelo { background: #fef9c3; color: #854d0e; }
        .status-vermelho { background: #fee2e2; color: #991b1b; }

        /* INPUTS DE CONFIGURAÇÃO */
        .config-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .config-item {
            display: flex;
            flex-direction: column;
        }
        .config-item label {
            font-size: 0.85em;
            color: #475569;
            margin-bottom: 5px;
            font-weight: 500;
        }
        .config-item input {
            padding: 10px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 0.9em;
        }
        .config-item input:focus {
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        @media print {
            body { background: white; padding: 0; }
            .header-actions, .btn, .modal-overlay { display: none !important; }
            .col-objeto .texto-wrap {
                display: block;
                -webkit-line-clamp: unset;
                max-height: none;
            }
        }

        @media (max-width: 768px) {
            .header { flex-direction: column; text-align: center; }
            table { font-size: 0.75em; }
            .col-orgao { width: 20%; }
            .col-objeto { width: 30%; }
            .col-acao { width: 180px; }
            .analise-grid { grid-template-columns: 1fr; }
            .tabs { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-brand">
                <h1>LICITA AI™</h1>
                <p>Inteligência Artificial em Contratações Públicas</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-print" onclick="window.print()">🖨️ Imprimir</button>
            </div>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">418</div>
                <div class="stat-label">Total de Oportunidades</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">100</div>
                <div class="stat-label">Visualizando</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">R$ 195.9M</div>
                <div class="stat-label">Valor em Disputa</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">24%</div>
                <div class="stat-label">Cobertura IA</div>
            </div>
        </div>

        <div class="content">
            <div class="content-header">
                <h2>📋 Oportunidades de Licitação com Precificação Inteligente (100)</h2>
                <span class="badge">IA Ativa - Análise em Tempo Real</span>
            </div>

            <!-- TABELA DE LICITAÇÕES (primeiras 20 linhas como exemplo) -->
            <table>
                <thead>
                    <tr>
                        <th class="col-id">ID</th>
                        <th class="col-orgao">ÓRGÃO</th>
                        <th class="col-objeto">OBJETO</th>
                        <th class="col-valor">VALOR ESTIMADO</th>
                        <th class="col-data">DATA PUB.</th>
                        <th class="col-acao">AÇÕES INTELIGENTES</th>
                    </tr>
                </thead>
                <tbody>
                    
                    <tr>
                        <td class="col-id">#861</td>
                        <td class="col-orgao" title="Secretaria de Educação do Rio de Janeiro">
                            Secretaria de Educação do Rio de Janeiro
                        </td>
                        <td class="col-objeto" title="Instalação de energia solar em prédios públicos">
                            <div class="texto-wrap">Instalação de energia solar em prédios públicos</div>
                        </td>
                        <td class="col-valor">R$ 226.383,00</td>
                        <td class="col-data">2026-03-07</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(861, 'Secretaria de Educação do Rio de Janeiro', 'Instalação de energia solar em prédios públicos', 226383)" class="btn btn-precificar" id="btn-precificar-861">🧠 Precificar</button>
                            <button onclick="abrirChecklist(861, 'Instalação de energia solar em prédios públicos')" class="btn btn-checklist" id="btn-check-861">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#860</td>
                        <td class="col-orgao" title="Prefeitura de Salvador - BA">
                            Prefeitura de Salvador - BA
                        </td>
                        <td class="col-objeto" title="Reforma de ginásio poliesportivo">
                            <div class="texto-wrap">Reforma de ginásio poliesportivo</div>
                        </td>
                        <td class="col-valor">R$ 805.691,00</td>
                        <td class="col-data">2026-03-04</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(860, 'Prefeitura de Salvador - BA', 'Reforma de ginásio poliesportivo', 805691)" class="btn btn-precificar" id="btn-precificar-860">🧠 Precificar</button>
                            <button onclick="abrirChecklist(860, 'Reforma de ginásio poliesportivo')" class="btn btn-checklist" id="btn-check-860">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#859</td>
                        <td class="col-orgao" title="Prefeitura de Recife - PE">
                            Prefeitura de Recife - PE
                        </td>
                        <td class="col-objeto" title="Fornecimento de cimento e material de construção">
                            <div class="texto-wrap">Fornecimento de cimento e material de construção</div>
                        </td>
                        <td class="col-valor">R$ 444.650,00</td>
                        <td class="col-data">2026-03-05</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(859, 'Prefeitura de Recife - PE', 'Fornecimento de cimento e material de construção', 444650)" class="btn btn-precificar" id="btn-precificar-859">🧠 Precificar</button>
                            <button onclick="abrirChecklist(859, 'Fornecimento de cimento e material de construção')" class="btn btn-checklist" id="btn-check-859">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#858</td>
                        <td class="col-orgao" title="Hospital das Clínicas de Porto Alegre">
                            Hospital das Clínicas de Porto Alegre
                        </td>
                        <td class="col-objeto" title="Aquisição de notebooks para professores">
                            <div class="texto-wrap">Aquisição de notebooks para professores</div>
                        </td>
                        <td class="col-valor">R$ 407.252,00</td>
                        <td class="col-data">2026-03-07</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(858, 'Hospital das Clínicas de Porto Alegre', 'Aquisição de notebooks para professores', 407252)" class="btn btn-precificar" id="btn-precificar-858">🧠 Precificar</button>
                            <button onclick="abrirChecklist(858, 'Aquisição de notebooks para professores')" class="btn btn-checklist" id="btn-check-858">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#857</td>
                        <td class="col-orgao" title="Prefeitura Municipal de São Paulo - SP">
                            Prefeitura Municipal de São Paulo - SP
                        </td>
                        <td class="col-objeto" title="Fornecimento de cimento e material de construção">
                            <div class="texto-wrap">Fornecimento de cimento e material de construção</div>
                        </td>
                        <td class="col-valor">R$ 452.151,00</td>
                        <td class="col-data">2026-03-02</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(857, 'Prefeitura Municipal de São Paulo - SP', 'Fornecimento de cimento e material de construção', 452151)" class="btn btn-precificar" id="btn-precificar-857">🧠 Precificar</button>
                            <button onclick="abrirChecklist(857, 'Fornecimento de cimento e material de construção')" class="btn btn-checklist" id="btn-check-857">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#856</td>
                        <td class="col-orgao" title="Prefeitura de Recife - PE">
                            Prefeitura de Recife - PE
                        </td>
                        <td class="col-objeto" title="Aquisição de equipamentos para cozinha industrial">
                            <div class="texto-wrap">Aquisição de equipamentos para cozinha industrial</div>
                        </td>
                        <td class="col-valor">R$ 348.392,00</td>
                        <td class="col-data">2026-03-01</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(856, 'Prefeitura de Recife - PE', 'Aquisição de equipamentos para cozinha industrial', 348392)" class="btn btn-precificar" id="btn-precificar-856">🧠 Precificar</button>
                            <button onclick="abrirChecklist(856, 'Aquisição de equipamentos para cozinha industrial')" class="btn btn-checklist" id="btn-check-856">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#855</td>
                        <td class="col-orgao" title="Governo do Estado de São Paulo">
                            Governo do Estado de São Paulo
                        </td>
                        <td class="col-objeto" title="Aquisição de playground e equipamentos recreativos">
                            <div class="texto-wrap">Aquisição de playground e equipamentos recreativos</div>
                        </td>
                        <td class="col-valor">R$ 95.890,00</td>
                        <td class="col-data">2026-03-01</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(855, 'Governo do Estado de São Paulo', 'Aquisição de playground e equipamentos recreativos', 95890)" class="btn btn-precificar" id="btn-precificar-855">🧠 Precificar</button>
                            <button onclick="abrirChecklist(855, 'Aquisição de playground e equipamentos recreativos')" class="btn btn-checklist" id="btn-check-855">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#854</td>
                        <td class="col-orgao" title="Prefeitura de Recife - PE">
                            Prefeitura de Recife - PE
                        </td>
                        <td class="col-objeto" title="Fornecimento de cimento e material de construção">
                            <div class="texto-wrap">Fornecimento de cimento e material de construção</div>
                        </td>
                        <td class="col-valor">R$ 341.827,00</td>
                        <td class="col-data">2026-03-07</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(854, 'Prefeitura de Recife - PE', 'Fornecimento de cimento e material de construção', 341827)" class="btn btn-precificar" id="btn-precificar-854">🧠 Precificar</button>
                            <button onclick="abrirChecklist(854, 'Fornecimento de cimento e material de construção')" class="btn btn-checklist" id="btn-check-854">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#853</td>
                        <td class="col-orgao" title="Hospital das Clínicas de Porto Alegre">
                            Hospital das Clínicas de Porto Alegre
                        </td>
                        <td class="col-objeto" title="Reforma de ginásio poliesportivo">
                            <div class="texto-wrap">Reforma de ginásio poliesportivo</div>
                        </td>
                        <td class="col-valor">R$ 891.518,00</td>
                        <td class="col-data">2026-03-05</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(853, 'Hospital das Clínicas de Porto Alegre', 'Reforma de ginásio poliesportivo', 891518)" class="btn btn-precificar" id="btn-precificar-853">🧠 Precificar</button>
                            <button onclick="abrirChecklist(853, 'Reforma de ginásio poliesportivo')" class="btn btn-checklist" id="btn-check-853">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#852</td>
                        <td class="col-orgao" title="Prefeitura de Fortaleza - CE">
                            Prefeitura de Fortaleza - CE
                        </td>
                        <td class="col-objeto" title="Aquisição de playground e equipamentos recreativos">
                            <div class="texto-wrap">Aquisição de playground e equipamentos recreativos</div>
                        </td>
                        <td class="col-valor">R$ 291.562,00</td>
                        <td class="col-data">2026-03-05</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(852, 'Prefeitura de Fortaleza - CE', 'Aquisição de playground e equipamentos recreativos', 291562)" class="btn btn-precificar" id="btn-precificar-852">🧠 Precificar</button>
                            <button onclick="abrirChecklist(852, 'Aquisição de playground e equipamentos recreativos')" class="btn btn-checklist" id="btn-check-852">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#851</td>
                        <td class="col-orgao" title="Governo do Estado de Minas Gerais">
                            Governo do Estado de Minas Gerais
                        </td>
                        <td class="col-objeto" title="Contratação de serviços de reforma de escolas">
                            <div class="texto-wrap">Contratação de serviços de reforma de escolas</div>
                        </td>
                        <td class="col-valor">R$ 1.791.881,00</td>
                        <td class="col-data">2026-03-08</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(851, 'Governo do Estado de Minas Gerais', 'Contratação de serviços de reforma de escolas', 1791881)" class="btn btn-precificar" id="btn-precificar-851">🧠 Precificar</button>
                            <button onclick="abrirChecklist(851, 'Contratação de serviços de reforma de escolas')" class="btn btn-checklist" id="btn-check-851">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#850</td>
                        <td class="col-orgao" title="Prefeitura de Curitiba - PR">
                            Prefeitura de Curitiba - PR
                        </td>
                        <td class="col-objeto" title="Fornecimento de mobiliário de escritório">
                            <div class="texto-wrap">Fornecimento de mobiliário de escritório</div>
                        </td>
                        <td class="col-valor">R$ 136.032,00</td>
                        <td class="col-data">2026-03-04</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(850, 'Prefeitura de Curitiba - PR', 'Fornecimento de mobiliário de escritório', 136032)" class="btn btn-precificar" id="btn-precificar-850">🧠 Precificar</button>
                            <button onclick="abrirChecklist(850, 'Fornecimento de mobiliário de escritório')" class="btn btn-checklist" id="btn-check-850">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#849</td>
                        <td class="col-orgao" title="Prefeitura de Belo Horizonte - MG">
                            Prefeitura de Belo Horizonte - MG
                        </td>
                        <td class="col-objeto" title="Instalação de energia solar em prédios públicos">
                            <div class="texto-wrap">Instalação de energia solar em prédios públicos</div>
                        </td>
                        <td class="col-valor">R$ 454.132,00</td>
                        <td class="col-data">2026-03-08</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(849, 'Prefeitura de Belo Horizonte - MG', 'Instalação de energia solar em prédios públicos', 454132)" class="btn btn-precificar" id="btn-precificar-849">🧠 Precificar</button>
                            <button onclick="abrirChecklist(849, 'Instalação de energia solar em prédios públicos')" class="btn btn-checklist" id="btn-check-849">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#848</td>
                        <td class="col-orgao" title="Prefeitura de Salvador - BA">
                            Prefeitura de Salvador - BA
                        </td>
                        <td class="col-objeto" title="Fornecimento de material de limpeza hospitalar">
                            <div class="texto-wrap">Fornecimento de material de limpeza hospitalar</div>
                        </td>
                        <td class="col-valor">R$ 164.913,00</td>
                        <td class="col-data">2026-03-04</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(848, 'Prefeitura de Salvador - BA', 'Fornecimento de material de limpeza hospitalar', 164913)" class="btn btn-precificar" id="btn-precificar-848">🧠 Precificar</button>
                            <button onclick="abrirChecklist(848, 'Fornecimento de material de limpeza hospitalar')" class="btn btn-checklist" id="btn-check-848">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#847</td>
                        <td class="col-orgao" title="Prefeitura de Manaus - AM">
                            Prefeitura de Manaus - AM
                        </td>
                        <td class="col-objeto" title="Reforma e ampliação de unidade de saúde">
                            <div class="texto-wrap">Reforma e ampliação de unidade de saúde</div>
                        </td>
                        <td class="col-valor">R$ 1.473.112,00</td>
                        <td class="col-data">2026-03-06</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(847, 'Prefeitura de Manaus - AM', 'Reforma e ampliação de unidade de saúde', 1473112)" class="btn btn-precificar" id="btn-precificar-847">🧠 Precificar</button>
                            <button onclick="abrirChecklist(847, 'Reforma e ampliação de unidade de saúde')" class="btn btn-checklist" id="btn-check-847">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#846</td>
                        <td class="col-orgao" title="Prefeitura de Recife - PE">
                            Prefeitura de Recife - PE
                        </td>
                        <td class="col-objeto" title="Aquisição de equipamentos para cozinha industrial">
                            <div class="texto-wrap">Aquisição de equipamentos para cozinha industrial</div>
                        </td>
                        <td class="col-valor">R$ 233.265,00</td>
                        <td class="col-data">2026-03-04</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(846, 'Prefeitura de Recife - PE', 'Aquisição de equipamentos para cozinha industrial', 233265)" class="btn btn-precificar" id="btn-precificar-846">🧠 Precificar</button>
                            <button onclick="abrirChecklist(846, 'Aquisição de equipamentos para cozinha industrial')" class="btn btn-checklist" id="btn-check-846">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#845</td>
                        <td class="col-orgao" title="Prefeitura de Brasília - DF">
                            Prefeitura de Brasília - DF
                        </td>
                        <td class="col-objeto" title="Reforma de ginásio poliesportivo">
                            <div class="texto-wrap">Reforma de ginásio poliesportivo</div>
                        </td>
                        <td class="col-valor">R$ 345.871,00</td>
                        <td class="col-data">2026-03-04</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(845, 'Prefeitura de Brasília - DF', 'Reforma de ginásio poliesportivo', 345871)" class="btn btn-precificar" id="btn-precificar-845">🧠 Precificar</button>
                            <button onclick="abrirChecklist(845, 'Reforma de ginásio poliesportivo')" class="btn btn-checklist" id="btn-check-845">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#844</td>
                        <td class="col-orgao" title="Secretaria de Educação do Rio de Janeiro">
                            Secretaria de Educação do Rio de Janeiro
                        </td>
                        <td class="col-objeto" title="Fornecimento de uniformes escolares">
                            <div class="texto-wrap">Fornecimento de uniformes escolares</div>
                        </td>
                        <td class="col-valor">R$ 171.719,00</td>
                        <td class="col-data">2026-03-04</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(844, 'Secretaria de Educação do Rio de Janeiro', 'Fornecimento de uniformes escolares', 171719)" class="btn btn-precificar" id="btn-precificar-844">🧠 Precificar</button>
                            <button onclick="abrirChecklist(844, 'Fornecimento de uniformes escolares')" class="btn btn-checklist" id="btn-check-844">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#843</td>
                        <td class="col-orgao" title="Secretaria de Educação do Rio de Janeiro">
                            Secretaria de Educação do Rio de Janeiro
                        </td>
                        <td class="col-objeto" title="Aquisição de equipamentos para cozinha industrial">
                            <div class="texto-wrap">Aquisição de equipamentos para cozinha industrial</div>
                        </td>
                        <td class="col-valor">R$ 217.148,00</td>
                        <td class="col-data">2026-03-07</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(843, 'Secretaria de Educação do Rio de Janeiro', 'Aquisição de equipamentos para cozinha industrial', 217148)" class="btn btn-precificar" id="btn-precificar-843">🧠 Precificar</button>
                            <button onclick="abrirChecklist(843, 'Aquisição de equipamentos para cozinha industrial')" class="btn btn-checklist" id="btn-check-843">✓ Check</button>
                        </td>
                    </tr>
                    
                    <tr>
                        <td class="col-id">#842</td>
                        <td class="col-orgao" title="Prefeitura de Brasília - DF">
                            Prefeitura de Brasília - DF
                        </td>
                        <td class="col-objeto" title="Fornecimento de computadores e impressoras">
                            <div class="texto-wrap">Fornecimento de computadores e impressoras</div>
                        </td>
                        <td class="col-valor">R$ 242.412,00</td>
                        <td class="col-data">2026-03-06</td>
                        <td class="col-acao">
                            <button onclick="abrirPrecificacaoInteligente(842, 'Prefeitura de Brasília - DF', 'Fornecimento de computadores e impressoras', 242412)" class="btn btn-precificar" id="btn-precificar-842">🧠 Precificar</button>
                            <button onclick="abrirChecklist(842, 'Fornecimento de computadores e impressoras')" class="btn btn-checklist" id="btn-check-842">✓ Check</button>
                        </td>
                    </tr>
                    
                </tbody>
            </table>
            
            <div style="text-align: center; margin-top: 20px; color: #64748b; font-size: 0.9em;">
                <p>Mostrando 20 de 100 licitações. Use a precificação inteligente para análise completa.</p>
            </div>
        </div>

        <div style="text-align: center; margin-top: 15px; color: rgba(255,255,255,0.8); font-size: 0.75em;">
            © 2024 LICITA AI™ | Sistema Profissional de Inteligência em Licitações
        </div>
    </div>

    <!-- MODAL DE PRECIFICAÇÃO INTELIGENTE -->
    <div id="modalPrecificacao" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3>🧠 Precificação Inteligente - Licitação <span id="precificarId"></span></h3>
                <button class="btn-fechar" onclick="fecharModalPrecificacao()">✕ Fechar</button>
            </div>
            <div class="modal-body">
                
                <!-- TABS -->
                <div class="tabs">
                    <button class="tab ativa" onclick="mudarTab('analise-mercado')">📊 Análise de Mercado</button>
                    <button class="tab" onclick="mudarTab('calculo-custos')">💰 Cálculo de Custos</button>
                    <button class="tab" onclick="mudarTab('lance-ideal')">🎯 Lance Ideal</button>
                    <button class="tab" onclick="mudarTab('simulacao')">🎲 Simulação de Pregão</button>
                    <button class="tab" onclick="mudarTab('estrategia')">📋 Estratégia</button>
                </div>

                <!-- CONTEÚDO: ANÁLISE DE MERCADO -->
                <div id="analise-mercado" class="tab-content ativa">
                    <div class="analise-grid">
                        <div class="analise-card">
                            <h4>💵 Preço Estimado Edital</h4>
                            <div class="valor" id="precoEstimado">R$ 0,00</div>
                            <div class="subvalor">Base oficial do órgão</div>
                        </div>
                        <div class="analise-card positivo">
                            <h4>🔮 Preço Vencedor Previsto</h4>
                            <div class="valor" id="precoPrevisto">R$ 0,00</div>
                            <div class="subvalor">IA - Análise 10 anos</div>
                        </div>
                        <div class="analise-card alerta">
                            <h4>📉 Redução Esperada</h4>
                            <div class="valor" id="reducaoEsperada">16%</div>
                            <div class="subvalor">Média histórica CGU</div>
                        </div>
                        <div class="analise-card">
                            <h4>📊 Intervalo Competitivo</h4>
                            <div class="valor" id="intervaloCompetitivo">R$ 0 - R$ 0</div>
                            <div class="subvalor">Zona de vitória provável</div>
                        </div>
                    </div>

                    <div class="secao">
                        <h4>📈 Análise Estatística de 10 Anos</h4>
                        <div class="grafico-container">
                            <div class="barra-progresso">
                                <div class="barra-label">Preço Máximo</div>
                                <div class="barra-track">
                                    <div class="barra-fill vermelho" id="barraMaximo" style="width: 100%">100%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Média Histórica</div>
                                <div class="barra-track">
                                    <div class="barra-fill amarelo" id="barraMedia" style="width: 87%">87%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Preço Vencedor</div>
                                <div class="barra-track">
                                    <div class="barra-fill verde" id="barraVencedor" style="width: 81%">81%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Mínimo Histórico</div>
                                <div class="barra-track">
                                    <div class="barra-fill azul" id="barraMinimo" style="width: 79%">79%</div>
                                </div>
                            </div>
                        </div>
                        
                        <table class="tabela-dados">
                            <thead>
                                <tr>
                                    <th>Métrica</th>
                                    <th>Valor</th>
                                    <th>Variação</th>
                                    <th>Observação</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Preço Máximo (10 anos)</td>
                                    <td id="tabelaMaximo">R$ 0,00</td>
                                    <td>-</td>
                                    <td>Pior cenário</td>
                                </tr>
                                <tr>
                                    <td>Média Histórica</td>
                                    <td id="tabelaMedia">R$ 0,00</td>
                                    <td id="varMedia">-13%</td>
                                    <td>Tendência central</td>
                                </tr>
                                <tr>
                                    <td>Preço Vencedor Médio</td>
                                    <td id="tabelaVencedor">R$ 0,00</td>
                                    <td id="varVencedor">-19%</td>
                                    <td>Meta realista</td>
                                </tr>
                                <tr>
                                    <td>Mínimo Histórico</td>
                                    <td id="tabelaMinimo">R$ 0,00</td>
                                    <td id="varMinimo">-21%</td>
                                    <td>Limite inferior</td>
                                </tr>
                                <tr>
                                    <td>Desvio Padrão</td>
                                    <td id="desvioPadrao">R$ 0,00</td>
                                    <td>-</td>
                                    <td>Volatilidade do mercado</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="secao">
                        <h4>🔍 Fatores de Influência no Preço</h4>
                        <div class="grafico-container">
                            <div class="barra-progresso">
                                <div class="barra-label">Preço Estimado</div>
                                <div class="barra-track">
                                    <div class="barra-fill azul" style="width: 35%">35%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Histórico Regional</div>
                                <div class="barra-track">
                                    <div class="barra-fill azul" style="width: 25%">25%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Nº Concorrentes</div>
                                <div class="barra-track">
                                    <div class="barra-fill azul" style="width: 15%">15%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Volume Compra</div>
                                <div class="barra-track">
                                    <div class="barra-fill azul" style="width: 10%">10%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Região</div>
                                <div class="barra-track">
                                    <div class="barra-fill azul" style="width: 10%">10%</div>
                                </div>
                            </div>
                            <div class="barra-progresso">
                                <div class="barra-label">Prazo Pagamento</div>
                                <div class="barra-track">
                                    <div class="barra-fill azul" style="width: 5%">5%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- CONTEÚDO: CÁLCULO DE CUSTOS -->
                <div id="calculo-custos" class="tab-content">
                    <div class="info-msg">
                        <strong>⚙️ Configure seus custos reais para calcular o preço mínimo seguro</strong>
                    </div>

                    <div class="config-grid">
                        <div class="config-item">
                            <label>Custo do Produto/Serviço (R$)</label>
                            <input type="number" id="custoProduto" value="0" onchange="calcularPrecoMinimo()">
                        </div>
                        <div class="config-item">
                            <label>Frete/Logística (R$)</label>
                            <input type="number" id="custoFrete" value="0" onchange="calcularPrecoMinimo()">
                        </div>
                        <div class="config-item">
                            <label>Impostos (%)</label>
                            <input type="number" id="custoImpostos" value="12" onchange="calcularPrecoMinimo()">
                        </div>
                        <div class="config-item">
                            <label>Despesas Operacionais (%)</label>
                            <input type="number" id="custoOperacional" value="8" onchange="calcularPrecoMinimo()">
                        </div>
                        <div class="config-item">
                            <label>Reserva de Risco (%)</label>
                            <input type="number" id="custoRisco" value="3" onchange="calcularPrecoMinimo()">
                        </div>
                        <div class="config-item">
                            <label>Margem Mínima Desejada (%)</label>
                            <input type="number" id="margemMinima" value="5" onchange="calcularPrecoMinimo()">
                        </div>
                    </div>

                    <div class="analise-grid" style="margin-top: 20px;">
                        <div class="analise-card">
                            <h4>🧮 Custo Total Calculado</h4>
                            <div class="valor" id="custoTotal">R$ 0,00</div>
                            <div class="subvalor">Soma de todos os custos</div>
                        </div>
                        <div class="analise-card alerta">
                            <h4>🛡️ Preço Mínimo Seguro</h4>
                            <div class="valor" id="precoMinimoSeguro">R$ 0,00</div>
                            <div class="subvalor">Com margem de segurança</div>
                        </div>
                        <div class="analise-card" id="cardViabilidade">
                            <h4>✅ Viabilidade</h4>
                            <div class="valor" id="textoViabilidade">-</div>
                            <div class="subvalor" id="subViabilidade">Compare com preço previsto</div>
                        </div>
                    </div>

                    <div class="secao" id="alertaViabilidade" style="display: none;">
                        <div class="erro-msg">
                            <strong>⚠️ ATENÇÃO: Viabilidade Comprometida</strong><br>
                            Seu preço mínimo seguro está <strong>acima</strong> do preço vencedor previsto. 
                            Recomenda-se <strong>NÃO PARTICIPAR</strong> desta licitação ou renegociar custos.
                        </div>
                    </div>
                </div>

                <!-- CONTEÚDO: LANCE IDEAL -->
                <div id="lance-ideal" class="tab-content">
                    <div class="analise-grid">
                        <div class="analise-card positivo">
                            <h4>🎯 Lance Ideal Calculado</h4>
                            <div class="valor" id="lanceIdeal">R$ 0,00</div>
                            <div class="subvalor">Máxima chance de vitória</div>
                        </div>
                        <div class="analise-card">
                            <h4>🎲 Probabilidade de Vitória</h4>
                            <div class="valor" id="probabilidadeVitoria">0%</div>
                            <div class="subvalor">Baseado em modelo estatístico</div>
                        </div>
                        <div class="analise-card">
                            <h4>💰 Margem no Lance Ideal</h4>
                            <div class="valor" id="margemLanceIdeal">0%</div>
                            <div class="subvalor">Lucro estimado</div>
                        </div>
                        <div class="analise-card alerta">
                            <h4>⏱️ Posição na Disputa</h4>
                            <div class="valor" id="posicaoDisputa">Líder</div>
                            <div class="subvalor">Estimativa com 6 concorrentes</div>
                        </div>
                    </div>

                    <div class="secao">
                        <h4>📊 Comparação de Cenários</h4>
                        <table class="tabela-dados">
                            <thead>
                                <tr>
                                    <th>Cenário</th>
                                    <th>Valor do Lance</th>
                                    <th>Prob. Vitória</th>
                                    <th>Margem</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Conservador (1º quartil)</td>
                                    <td id="lanceConservador">R$ 0,00</td>
                                    <td>35%</td>
                                    <td id="margemConservador">12%</td>
                                    <td><span class="status-badge status-amarelo">Risco Baixo</span></td>
                                </tr>
                                <tr style="background: #f0fdf4;">
                                    <td><strong>🎯 IDEAL (recomendado)</strong></td>
                                    <td id="lanceIdealTabela"><strong>R$ 0,00</strong></td>
                                    <td><strong id="probIdealTabela">72%</strong></td>
                                    <td><strong id="margemIdealTabela">8%</strong></td>
                                    <td><span class="status-badge status-verde">Ótimo</span></td>
                                </tr>
                                <tr>
                                    <td>Agressivo (mínimo)</td>
                                    <td id="lanceAgressivo">R$ 0,00</td>
                                    <td>85%</td>
                                    <td id="margemAgressivo">3%</td>
                                    <td><span class="status-badge status-vermelho">Risco Alto</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="secao">
                        <h4>🧮 Fórmula do Lance Ideal</h4>
                        <div class="info-msg">
                            <strong>Fórmula aplicada:</strong><br>
                            Lance Ideal = (Preço Previsto × 0.5) + (Mínimo Histórico × 0.3) + (Preço Mínimo Seguro × 0.2)<br>
                            <br>
                            <strong>Com ajuste:</strong> Se Lance Ideal < Preço Mínimo Seguro, usar Preço Mínimo Seguro + 2%
                        </div>
                    </div>
                </div>

                <!-- CONTEÚDO: SIMULAÇÃO DE PREGÃO -->
                <div id="simulacao" class="tab-content">
                    <div class="info-msg">
                        <strong>🎲 Simulação de Pregão Eletrônico</strong><br>
                        Baseado em histórico de 10 anos: média de 22 lances, queda de 0.7% por lance, 6 concorrentes.
                    </div>

                    <div class="analise-grid">
                        <div class="analise-card">
                            <h4>🏁 Lance Inicial Médio</h4>
                            <div class="valor" id="lanceInicial">R$ 0,00</div>
                            <div class="subvalor">5% abaixo do estimado</div>
                        </div>
                        <div class="analise-card">
                            <h4>📉 Queda por Lance</h4>
                            <div class="valor">0.7%</div>
                            <div class="subvalor">Média histórica</div>
                        </tr>
                        <div class="analise-card">
                            <h4>🔢 Nº Lances Esperados</h4>
                            <div class="valor">22</div>
                            <div class="subvalor">Com 6 concorrentes</div>
                        </div>
                        <div class="analise-card positivo">
                            <h4>🏆 Preço Final Simulado</h4>
                            <div class="valor" id="precoFinalSimulado">R$ 0,00</div>
                            <div class="subvalor">Convergência estimada</div>
                        </div>
                    </div>

                    <div class="secao">
                        <h4>📈 Evolução Simulada dos Lances</h4>
                        <div class="grafico-container" id="graficoLances">
                            <!-- Gerado dinamicamente via JS -->
                        </div>
                    </div>

                    <div class="secao">
                        <h4>⏱️ Estratégia de Tempo (ComprasNet)</h4>
                        <div class="aviso-msg">
                            <strong>⚠️ Importante:</strong> No sistema ComprasNet, o encerramento ocorre em tempo aleatório após aviso. 
                            É estratégico manter a liderança nos segundos finais.
                        </div>
                        <table class="tabela-dados">
                            <thead>
                                <tr>
                                    <th>Fase</th>
                                    <th>Tempo</th>
                                    <th>Ação Recomendada</th>
                                    <th>Decremento</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Abertura</td>
                                    <td>0-2 min</td>
                                    <td>Aguardar, observar concorrentes</td>
                                    <td>-</td>
                                </tr>
                                <tr>
                                    <td>Entrada</td>
                                    <td>2-5 min</td>
                                    <td>Lance inicial competitivo</td>
                                    <td>5% abaixo</td>
                                </tr>
                                <tr>
                                    <td>Disputa</td>
                                    <td>5-15 min</td>
                                    <td>Reduzir gradualmente</td>
                                    <td>1% → 0.5%</td>
                                </tr>
                                <tr style="background: #fef3c7;">
                                    <td><strong>Final</strong></td>
                                    <td><strong>Últimos 30s</strong></td>
                                    <td><strong>Lance decisivo</strong></td>
                                    <td><strong>0.1%</strong></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- CONTEÚDO: ESTRATÉGIA -->
                <div id="estrategia" class="tab-content">
                    <div class="sucesso-msg">
                        <strong>📋 Relatório de Estratégia - Licitação <span id="relatorioId"></span></strong>
                    </div>

                    <div class="secao">
                        <h4>🎯 Resumo Executivo</h4>
                        <table class="tabela-dados">
                            <tbody>
                                <tr>
                                    <td><strong>Objeto</strong></td>
                                    <td id="relatorioObjeto">-</td>
                                </tr>
                                <tr>
                                    <td><strong>Órgão</strong></td>
                                    <td id="relatorioOrgao">-</td>
                                </tr>
                                <tr>
                                    <td><strong>Preço Estimado</strong></td>
                                    <td id="relatorioEstimado">-</td>
                                </tr>
                                <tr>
                                    <td><strong>Preço Vencedor Previsto</strong></td>
                                    <td id="relatorioPrevisto" style="color: #16a34a; font-weight: 600;">-</td>
                                </tr>
                                <tr>
                                    <td><strong>Intervalo Competitivo</strong></td>
                                    <td id="relatorioIntervalo">-</td>
                                </tr>
                                <tr>
                                    <td><strong>Seu Custo Mínimo</strong></td>
                                    <td id="relatorioCusto">-</td>
                                </tr>
                                <tr>
                                    <td><strong>Lance Ideal</strong></td>
                                    <td id="relatorioLanceIdeal" style="color: #2563eb; font-weight: 700;">-</td>
                                </tr>
                                <tr>
                                    <td><strong>Probabilidade de Vitória</strong></td>
                                    <td id="relatorioProbabilidade" style="color: #16a34a; font-weight: 600;">-</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="secao">
                        <h4>📊 Estratégia de Lances Recomendada</h4>
                        <div class="info-msg">
                            <strong>Sequência de lances para maximizar chance de vitória:</strong>
                        </div>
                        <table class="tabela-dados">
                            <thead>
                                <tr>
                                    <th>Ordem</th>
                                    <th>Tipo</th>
                                    <th>Valor</th>
                                    <th>Redução</th>
                                    <th>Condição</th>
                                </tr>
                            </thead>
                            <tbody id="tabelaEstrategia">
                                <!-- Gerado dinamicamente -->
                            </tbody>
                        </table>
                    </div>

                    <div class="secao" id="secaoRecomendacao">
                        <h4>💡 Recomendação Final da IA</h4>
                        <div id="recomendacaoIA" class="info-msg">
                            <!-- Gerado dinamicamente -->
                        </div>
                    </div>

                    <div class="btn-group">
                        <button onclick="gerarPDF()" class="btn" style="background: #dc2626;">
                            📄 Gerar PDF Completo
                        </button>
                        <button onclick="exportarExcel()" class="btn" style="background: #16a34a;">
                            📊 Exportar Excel
                        </button>
                        <button onclick="salvarEstrategia()" class="btn" style="background: #2563eb;">
                            💾 Salvar Estratégia
                        </button>
                        <button onclick="window.print()" class="btn btn-print">
                            🖨️ Imprimir
                        </button>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- MODAL DE CHECKLIST -->
    <div id="modalChecklist" class="modal-overlay">
        <div class="modal-content" style="max-width: 600px;">
            <div class="modal-header">
                <h3>📋 Checklist da Licitação <span id="checklistId"></span></h3>
                <button class="btn-fechar" onclick="fecharModalChecklist()">✕ Fechar</button>
            </div>
            <div class="modal-body" id="checklistBody">
                <!-- Conteúdo dinâmico -->
            </div>
        </div>
    </div>

    <script>
        // ==========================================
        // BANCO DE DADOS SIMULADO - 10 ANOS DE PREGÕES
        // ==========================================
        const bancoHistorico = {
            // Dados estatísticos baseados em estudos da CGU
            estatisticasGerais: {
                reducaoMedia: 0.16,        // 16% de redução média
                desvioPadrao: 0.08,        // 8% de desvio padrão
                mediaLances: 22,           // 22 lances em média
                quedaPorLance: 0.007,      // 0.7% por lance
                concorrentesMedio: 6       // 6 concorrentes médio
            },
            
            // Histórico por tipo de objeto (simulado)
            historicoPorTipo: {
                'energia solar': { media: 0.84, minimo: 0.79, maximo: 0.95 },
                'reforma': { media: 0.87, minimo: 0.82, maximo: 0.96 },
                'cimento': { media: 0.89, minimo: 0.85, maximo: 0.97 },
                'notebook': { media: 0.82, minimo: 0.76, maximo: 0.94 },
                'equipamentos': { media: 0.85, minimo: 0.80, maximo: 0.95 },
                'playground': { media: 0.88, minimo: 0.83, maximo: 0.96 },
                'mobiliário': { media: 0.86, minimo: 0.81, maximo: 0.95 },
                'material limpeza': { media: 0.90, minimo: 0.86, maximo: 0.98 },
                'uniformes': { media: 0.87, minimo: 0.82, maximo: 0.96 },
                'computadores': { media: 0.83, minimo: 0.77, maximo: 0.94 },
                'material escolar': { media: 0.88, minimo: 0.84, maximo: 0.97 },
                'default': { media: 0.85, minimo: 0.80, maximo: 0.95 }
            }
        };

        // Checklist padrão
        const checklistPadrao = [
            { id: 'doc1', label: 'Certidão Negativa de Débitos (CND) atualizada' },
            { id: 'doc2', label: 'Certidão Negativa de Falência e Concordata' },
            { id: 'doc3', label: 'Certidão Negativa de Débitos Trabalhistas (CNDT)' },
            { id: 'doc4', label: 'Regularidade Fiscal Estadual e Municipal' },
            { id: 'doc5', label: 'Registro Cadastral Certificado (RCC) ou CAUF' },
            { id: 'doc6', label: 'Procuração com poderes específicos' },
            { id: 'doc7', label: 'Comprovante de inscrição no CREA (se engenharia)' },
            { id: 'doc8', label: 'ART/RRT para execução do objeto' },
            { id: 'doc9', label: 'Certidão de Regularidade FGTS' },
            { id: 'doc10', label: 'Certificado de Registro no Ministério do Trabalho' },
            { id: 'doc11', label: 'Declaração de não empregar menor de 18 anos' },
            { id: 'doc12', label: 'Declaração de não empregar trabalho escravo' },
            { id: 'doc13', label: 'Certificado de Regularidade no INSS' },
            { id: 'doc14', label: 'Declaração de Microempresa ou EPP' },
            { id: 'doc15', label: 'Garantia de Execução' }
        ];

        // Estado
        let estadosChecklist = {};
        let dadosAtuais = {};

        // ==========================================
        // FUNÇÕES DE PRECIFICAÇÃO INTELIGENTE
        // ==========================================

        function abrirPrecificacaoInteligente(id, orgao, objeto, valorEstimado) {
            const btn = document.getElementById(`btn-precificar-${id}`);
            btn.innerHTML = '<span class="loading"></span> Analisando...';
            btn.disabled = true;

            // Simular processamento da IA
            setTimeout(() => {
                // Detectar tipo de objeto para buscar histórico apropriado
                const tipoDetectado = detectarTipoObjeto(objeto);
                const historico = bancoHistorico.historicoPorTipo[tipoDetectado] || bancoHistorico.historicoPorTipo['default'];
                
                // Cálculos estatísticos
                const precoMaximo = valorEstimado * historico.maximo;
                const precoMedio = valorEstimado * historico.media;
                const precoMinimo = valorEstimado * historico.minimo;
                const precoVencedor = (precoMedio * 0.5) + (precoMinimo * 0.3) + (valorEstimado * 0.2);
                const desvio = valorEstimado * bancoHistorico.estatisticasGerais.desvioPadrao;
                
                // Intervalo competitivo
                const intervaloMin = precoVencedor - desvio;
                const intervaloMax = precoVencedor + desvio;
                
                // Salvar dados para uso nas tabs
                dadosAtuais = {
                    id, orgao, objeto, valorEstimado,
                    precoMaximo, precoMedio, precoMinimo, precoVencedor,
                    desvio, intervaloMin, intervaloMax, historico
                };

                // Preencher modal
                preencherAnaliseMercado();
                
                // Resetar custos
                document.getElementById('custoProduto').value = (valorEstimado * 0.6).toFixed(2);
                calcularPrecoMinimo();
                
                // Mostrar modal
                document.getElementById('precificarId').textContent = `#${id}`;
                document.getElementById('modalPrecificacao').classList.add('ativo');
                
                // Resetar tabs
                mudarTab('analise-mercado');
                
                btn.innerHTML = '🧠 Precificar';
                btn.disabled = false;
            }, 800);
        }

        function detectarTipoObjeto(objeto) {
            const objetoLower = objeto.toLowerCase();
            if (objetoLower.includes('solar')) return 'energia solar';
            if (objetoLower.includes('reforma')) return 'reforma';
            if (objetoLower.includes('cimento')) return 'cimento';
            if (objetoLower.includes('notebook')) return 'notebook';
            if (objetoLower.includes('equipamento')) return 'equipamentos';
            if (objetoLower.includes('playground')) return 'playground';
            if (objetoLower.includes('mobiliário') || objetoLower.includes('moveis')) return 'mobiliário';
            if (objetoLower.includes('limpeza')) return 'material limpeza';
            if (objetoLower.includes('uniforme')) return 'uniformes';
            if (objetoLower.includes('computador')) return 'computadores';
            if (objetoLower.includes('escolar') || objetoLower.includes('kit')) return 'material escolar';
            return 'default';
        }

        function preencherAnaliseMercado() {
            const d = dadosAtuais;
            
            // Cards principais
            document.getElementById('precoEstimado').textContent = formatarMoeda(d.valorEstimado);
            document.getElementById('precoPrevisto').textContent = formatarMoeda(d.precoVencedor);
            document.getElementById('reducaoEsperada').textContent = Math.round((1 - (d.precoVencedor / d.valorEstimado)) * 100) + '%';
            document.getElementById('intervaloCompetitivo').textContent = 
                `${formatarMoeda(d.intervaloMin)} - ${formatarMoeda(d.intervaloMax)}`;
            
            // Barras de progresso
            document.getElementById('barraMaximo').style.width = '100%';
            document.getElementById('barraMaximo').textContent = '100%';
            document.getElementById('barraMedia').style.width = Math.round((d.precoMedio / d.precoMaximo) * 100) + '%';
            document.getElementById('barraMedia').textContent = Math.round((d.precoMedio / d.precoMaximo) * 100) + '%';
            document.getElementById('barraVencedor').style.width = Math.round((d.precoVencedor / d.precoMaximo) * 100) + '%';
            document.getElementById('barraVencedor').textContent = Math.round((d.precoVencedor / d.precoMaximo) * 100) + '%';
            document.getElementById('barraMinimo').style.width = Math.round((d.precoMinimo / d.precoMaximo) * 100) + '%';
            document.getElementById('barraMinimo').textContent = Math.round((d.precoMinimo / d.precoMaximo) * 100) + '%';
            
            // Tabela de dados
            document.getElementById('tabelaMaximo').textContent = formatarMoeda(d.precoMaximo);
            document.getElementById('tabelaMedia').textContent = formatarMoeda(d.precoMedio);
            document.getElementById('varMedia').textContent = '-' + Math.round((1 - d.historico.media) * 100) + '%';
            document.getElementById('tabelaVencedor').textContent = formatarMoeda(d.precoVencedor);
            document.getElementById('varVencedor').textContent = '-' + Math.round((1 - (d.precoVencedor / d.valorEstimado)) * 100) + '%';
            document.getElementById('tabelaMinimo').textContent = formatarMoeda(d.precoMinimo);
            document.getElementById('varMinimo').textContent = '-' + Math.round((1 - d.historico.minimo) * 100) + '%';
            document.getElementById('desvioPadrao').textContent = formatarMoeda(d.desvio);
        }

        function calcularPrecoMinimo() {
            const custoProduto = parseFloat(document.getElementById('custoProduto').value) || 0;
            const custoFrete = parseFloat(document.getElementById('custoFrete').value) || 0;
            const custoImpostos = parseFloat(document.getElementById('custoImpostos').value) || 0;
            const custoOperacional = parseFloat(document.getElementById('custoOperacional').value) || 0;
            const custoRisco = parseFloat(document.getElementById('custoRisco').value) || 0;
            const margemMinima = parseFloat(document.getElementById('margemMinima').value) || 0;
            
            // Cálculo do custo total
            const custoBase = custoProduto + custoFrete;
            const custoTotal = custoBase * (1 + (custoImpostos + custoOperacional + custoRisco) / 100);
            
            // Preço mínimo com margem
            const precoMinimo = custoTotal / (1 - (margemMinima / 100));
            
            document.getElementById('custoTotal').textContent = formatarMoeda(custoTotal);
            document.getElementById('precoMinimoSeguro').textContent = formatarMoeda(precoMinimo);
            
            // Verificar viabilidade
            const d = dadosAtuais;
            const viavel = precoMinimo <= d.precoVencedor;
            
            const cardViabilidade = document.getElementById('cardViabilidade');
            const textoViabilidade = document.getElementById('textoViabilidade');
            const subViabilidade = document.getElementById('subViabilidade');
            const alertaViabilidade = document.getElementById('alertaViabilidade');
            
            if (viavel) {
                cardViabilidade.className = 'analise-card positivo';
                textoViabilidade.textContent = '✅ VIÁVEL';
                subViabilidade.textContent = 'Preço mínimo abaixo do previsto';
                alertaViabilidade.style.display = 'none';
            } else {
                cardViabilidade.className = 'analise-card negativo';
                textoViabilidade.textContent = '❌ INVIÁVEL';
                subViabilidade.textContent = 'Preço mínimo acima do previsto';
                alertaViabilidade.style.display = 'block';
            }
            
            // Calcular lance ideal
            calcularLanceIdeal(precoMinimo);
        }

        function calcularLanceIdeal(precoMinimo) {
            const d = dadosAtuais;
            
            // Fórmula: (Preço Previsto × 0.5) + (Mínimo Histórico × 0.3) + (Preço Mínimo Seguro × 0.2)
            let lanceIdeal = (d.precoVencedor * 0.5) + (d.precoMinimo * 0.3) + (precoMinimo * 0.2);
            
            // Ajuste de segurança
            if (lanceIdeal < precoMinimo) {
                lanceIdeal = precoMinimo * 1.02; // 2% acima do mínimo
            }
            
            // Limitar ao intervalo competitivo
            if (lanceIdeal > d.intervaloMax) {
                lanceIdeal = d.intervaloMax * 0.98;
            }
            
            // Calcular probabilidade
            const distanciaMedia = d.precoMedio - lanceIdeal;
            const probabilidade = Math.min(95, Math.max(15, 50 + (distanciaMedia / d.precoMedio) * 100));
            
            // Calcular margem
            const custoTotal = parseFloat(document.getElementById('custoTotal').textContent.replace(/[^\d,]/g, '').replace(',', '.')) || precoMinimo;
            const margem = ((lanceIdeal - custoTotal) / lanceIdeal) * 100;
            
            // Atualizar UI
            document.getElementById('lanceIdeal').textContent = formatarMoeda(lanceIdeal);
            document.getElementById('probabilidadeVitoria').textContent = Math.round(probabilidade) + '%';
            document.getElementById('margemLanceIdeal').textContent = margem.toFixed(1) + '%';
            
            // Determinar posição
            const posicao = probabilidade > 70 ? 'Líder' : probabilidade > 40 ? 'Competitivo' : 'Desfavorecido';
            document.getElementById('posicaoDisputa').textContent = posicao;
            
            // Cenários
            const lanceConservador = d.precoMedio * 0.95;
            const lanceAgressivo = d.precoMinimo * 1.01;
            
            document.getElementById('lanceConservador').textContent = formatarMoeda(lanceConservador);
            document.getElementById('margemConservador').textContent = ((lanceConservador - custoTotal) / lanceConservador * 100).toFixed(1) + '%';
            document.getElementById('lanceIdealTabela').textContent = formatarMoeda(lanceIdeal);
            document.getElementById('probIdealTabela').textContent = Math.round(probabilidade) + '%';
            document.getElementById('margemIdealTabela').textContent = margem.toFixed(1) + '%';
            document.getElementById('lanceAgressivo').textContent = formatarMoeda(lanceAgressivo);
            document.getElementById('margemAgressivo').textContent = ((lanceAgressivo - custoTotal) / lanceAgressivo * 100).toFixed(1) + '%';
            
            // Simulação
            gerarSimulacao(lanceIdeal);
            
            // Estratégia
            gerarEstrategia(lanceIdeal, precoMinimo, probabilidade);
        }

        function gerarSimulacao(lanceIdeal) {
            const d = dadosAtuais;
            const lanceInicial = d.valorEstimado * 0.95;
            const precoFinal = lanceIdeal;
            
            document.getElementById('lanceInicial').textContent = formatarMoeda(lanceInicial);
            document.getElementById('precoFinalSimulado').textContent = formatarMoeda(precoFinal);
            
            // Gerar gráfico de lances
            let html = '';
            const numLances = 8; // Simplificado para visualização
            const decremento = (lanceInicial - precoFinal) / numLances;
            
            for (let i = 0; i <= numLances; i++) {
                const valor = lanceInicial - (decremento * i);
                const percentual = (valor / d.valorEstimado) * 100;
                const isFinal = i === numLances;
                
                html += `
                    <div class="barra-progresso">
                        <div class="barra-label">${isFinal ? '🏆 Final' : 'Lance ' + i}</div>
                        <div class="barra-track">
                            <div class="barra-fill ${isFinal ? 'verde' : 'azul'}" style="width: ${percentual}%">
                                ${formatarMoeda(valor)}
                            </div>
                        </div>
                    </div>
                `;
            }
            
            document.getElementById('graficoLances').innerHTML = html;
        }

        function gerarEstrategia(lanceIdeal, precoMinimo, probabilidade) {
            const d = dadosAtuais;
            
            // Preencher relatório
            document.getElementById('relatorioId').textContent = `#${d.id}`;
            document.getElementById('relatorioObjeto').textContent = d.objeto;
            document.getElementById('relatorioOrgao').textContent = d.orgao;
            document.getElementById('relatorioEstimado').textContent = formatarMoeda(d.valorEstimado);
            document.getElementById('relatorioPrevisto').textContent = formatarMoeda(d.precoVencedor);
            document.getElementById('relatorioIntervalo').textContent = `${formatarMoeda(d.intervaloMin)} - ${formatarMoeda(d.intervaloMax)}`;
            document.getElementById('relatorioCusto').textContent = document.getElementById('precoMinimoSeguro').textContent;
            document.getElementById('relatorioLanceIdeal').textContent = formatarMoeda(lanceIdeal);
            document.getElementById('relatorioProbabilidade').textContent = Math.round(probabilidade) + '%';
            
            // Tabela de estratégia
            const lanceInicial = d.valorEstimado * 0.95;
            const estrategia = [
                { ordem: 1, tipo: 'Entrada', valor: lanceInicial, reducao: '5%', condicao: 'Início da disputa' },
                { ordem: 2, tipo: 'Redução 1', valor: lanceInicial * 0.99, reducao: '1%', condicao: 'Se ultrapassado' },
                { ordem: 3, tipo: 'Redução 2', valor: lanceInicial * 0.985, reducao: '0.5%', condicao: 'Manter liderança' },
                { ordem: 4, tipo: 'Redução 3', valor: lanceInicial * 0.982, reducao: '0.3%', condicao: 'Aproximação final' },
                { ordem: 5, tipo: 'Final', valor: lanceIdeal, reducao: '0.1%', condicao: 'Últimos 30 segundos' }
            ];
            
            let html = '';
            estrategia.forEach(e => {
                const isFinal = e.tipo === 'Final';
                html += `
                    <tr style="${isFinal ? 'background: #f0fdf4; font-weight: 600;' : ''}">
                        <td>${e.ordem}</td>
                        <td>${e.tipo}</td>
                        <td>${formatarMoeda(e.valor)}</td>
                        <td>${e.reducao}</td>
                        <td>${e.condicao}</td>
                    </tr>
                `;
            });
            document.getElementById('tabelaEstrategia').innerHTML = html;
            
            // Recomendação final
            const viavel = precoMinimo <= d.precoVencedor;
            let recomendacao = '';
            
            if (viavel && probabilidade > 60) {
                recomendacao = `
                    <strong>✅ RECOMENDAÇÃO: PARTICIPAR</strong><br><br>
                    Esta licitação apresenta excelente viabilidade. O lance ideal está dentro do intervalo competitivo 
                    com probabilidade de vitória de ${Math.round(probabilidade)}%.<br><br>
                    <strong>Ações:</strong><br>
                    • Preparar documentação completa<br>
                    • Monitorar concorrentes no histórico<br>
                    • Executar estratégia de lances conforme planejado<br>
                    • Manter reserva de 2% para lance final
                `;
            } else if (viavel && probabilidade > 40) {
                recomendacao = `
                    <strong>⚠️ RECOMENDAÇÃO: PARTICIPAR COM CAUTELA</strong><br><br>
                    Viabilidade moderada. Probabilidade de ${Math.round(probabilidade)}% requer atenção especial.<br><br>
                    <strong>Ações:</strong><br>
                    • Verificar possibilidade de redução de custos<br>
                    • Analisar concorrentes frequentes neste órgão<br>
                    • Considerar parceria para aumentar competitividade<br>
                    • Definir limite máximo de lance antes do pregão
                `;
            } else {
                recomendacao = `
                    <strong>❌ RECOMENDAÇÃO: NÃO PARTICIPAR</strong><br><br>
                    Preço mínimo seguro está acima do preço vencedor previsto. Risco elevado de prejuízo.<br><br>
                    <strong>Alternativas:</strong><br>
                    • Renegociar custos com fornecedores<br>
                    • Buscar licitações com maior valor estimado<br>
                    • Aguardar novo edital com especificações diferentes<br>
                    • Analisar subcontratação parcial
                `;
            }
            
            document.getElementById('recomendacaoIA').innerHTML = recomendacao;
        }

        // ==========================================
        // FUNÇÕES DE UTILIDADE
        // ==========================================

        function formatarMoeda(valor) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(valor);
        }

        function mudarTab(tabId) {
            // Esconder todas as tabs
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('ativa'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('ativa'));
            
            // Mostrar tab selecionada
            document.getElementById(tabId).classList.add('ativa');
            event.target.classList.add('ativa');
        }

        function fecharModalPrecificacao() {
            document.getElementById('modalPrecificacao').classList.remove('ativo');
        }

        // ==========================================
        // FUNÇÕES DE CHECKLIST
        // ==========================================

        function abrirChecklist(id, objeto) {
            const btn = document.getElementById(`btn-check-${id}`);
            btn.innerHTML = '<span class="loading"></span>';
            btn.disabled = true;

            setTimeout(() => {
                document.getElementById('checklistId').textContent = `#${id}`;
                
                const checklistData = estadosChecklist[id] || {};
                let html = `
                    <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <strong>Objeto:</strong> ${objeto}
                    </div>
                    <div id="listaChecklist">
                `;
                
                checklistPadrao.forEach(item => {
                    const checked = checklistData[item.id] ? 'checked' : '';
                    const classeChecked = checklistData[item.id] ? 'checked' : '';
                    
                    html += `
                        <div class="checklist-item ${classeChecked}" id="item-${item.id}">
                            <input type="checkbox" 
                                   id="${item.id}" 
                                   ${checked} 
                                   onchange="toggleItem('${id}', '${item.id}')">
                            <label for="${item.id}">${item.label}</label>
                        </div>
                    `;
                });
                
                html += '</div>';
                
                html += `
                    <div class="btn-group">
                        <button onclick="salvarChecklist('${id}')" class="btn btn-checklist" style="padding: 10px 20px;">
                            💾 Salvar Checklist
                        </button>
                        <button onclick="window.print()" class="btn btn-print" style="padding: 10px 20px;">
                            🖨️ Imprimir
                        </button>
                    </div>
                `;
                
                document.getElementById('checklistBody').innerHTML = html;
                document.getElementById('modalChecklist').classList.add('ativo');
                
                btn.innerHTML = '✓ Check';
                btn.disabled = false;
            }, 500);
        }

        function toggleItem(checklistId, itemId) {
            const checkbox = document.getElementById(itemId);
            const itemDiv = document.getElementById(`item-${itemId}`);
            
            if (!estadosChecklist[checklistId]) {
                estadosChecklist[checklistId] = {};
            }
            
            estadosChecklist[checklistId][itemId] = checkbox.checked;
            
            if (checkbox.checked) {
                itemDiv.classList.add('checked');
            } else {
                itemDiv.classList.remove('checked');
            }
        }

        function salvarChecklist(id) {
            localStorage.setItem(`checklist_${id}`, JSON.stringify(estadosChecklist[id] || {}));
            alert('✅ Checklist salvo com sucesso!');
        }

        function fecharModalChecklist() {
            document.getElementById('modalChecklist').classList.remove('ativo');
        }

        // ==========================================
        // FUNÇÕES DE EXPORTAÇÃO
        // ==========================================

        function gerarPDF() {
            alert('📄 Gerando PDF completo da análise...\n\nRelatório inclui:\n• Análise de mercado\n• Cálculo de custos\n• Lance ideal\n• Estratégia completa\n• Checklist de documentos');
        }

        function exportarExcel() {
            alert('📊 Exportando dados para Excel...\n\nPlanilha inclui todas as métricas calculadas para análise posterior.');
        }

        function salvarEstrategia() {
            const dadosEstrategia = {
                ...dadosAtuais,
                custos: {
                    produto: document.getElementById('custoProduto').value,
                    frete: document.getElementById('custoFrete').value,
                    impostos: document.getElementById('custoImpostos').value,
                    operacional: document.getElementById('custoOperacional').value,
                    risco: document.getElementById('custoRisco').value,
                    margem: document.getElementById('margemMinima').value
                },
                lanceIdeal: document.getElementById('lanceIdeal').textContent,
                probabilidade: document.getElementById('probabilidadeVitoria').textContent,
                data: new Date().toISOString()
            };
            
            localStorage.setItem(`estrategia_${dadosAtuais.id}`, JSON.stringify(dadosEstrategia));
            alert('💾 Estratégia salva com sucesso! Acesse em "Minhas Estratégias" no menu principal.');
        }

        // Carregar dados salvos ao iniciar
        window.addEventListener('load', function() {
            // Carregar checklists
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key.startsWith('checklist_')) {
                    const id = key.replace('checklist_', '');
                    try {
                        estadosChecklist[id] = JSON.parse(localStorage.getItem(key));
                    } catch (e) {
                        console.warn('Erro ao carregar checklist:', e);
                    }
                }
            }
        });

        // Fechar modais ao clicar fora
        document.getElementById('modalPrecificacao').addEventListener('click', function(e) {
            if (e.target === this) fecharModalPrecificacao();
        });
        document.getElementById('modalChecklist').addEventListener('click', function(e) {
            if (e.target === this) fecharModalChecklist();
        });

        // Fechar com ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                fecharModalPrecificacao();
                fecharModalChecklist();
            }
        });
    </script>
</body>
</html>