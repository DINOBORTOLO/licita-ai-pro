from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import stripe
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-secreta-desenvolvimento')

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================

# Usar DATABASE_URL se disponível (Render), senão SQLite local
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Render ou PostgreSQL
    if database_url.startswith('postgres'):
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace('postgres://', 'postgresql://')
        print("🐘 Usando PostgreSQL")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"💾 Usando SQLite: {database_url}")
else:
    # Local - garantir que pasta data existe
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'usuarios.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print(f"💻 Local: {db_path}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_...')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_...')

# Inicialização de extensões
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# ==========================================
# MODELOS DE BANCO DE DADOS
# ==========================================

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(150))
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    
    tipo = db.Column(db.String(20), default='cliente')
    plano = db.Column(db.String(50), default='gratuito')
    status_assinatura = db.Column(db.String(20), default='ativo')
    
    stripe_customer_id = db.Column(db.String(100))
    stripe_subscription_id = db.Column(db.String(100))
    
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    data_ultimo_acesso = db.Column(db.DateTime)
    data_expiracao = db.Column(db.DateTime)
    
    licitacoes_consultadas = db.Column(db.Integer, default=0)
    limite_consultas = db.Column(db.Integer, default=10)
    
    notificacoes_email = db.Column(db.Boolean, default=True)
    alertas_ativos = db.Column(db.JSON, default=list)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.tipo in ['admin', 'superadmin']
    
    def is_superadmin(self):
        return self.tipo == 'superadmin'
    
    def has_active_subscription(self):
        if self.plano == 'gratuito':
            return True
        return self.status_assinatura == 'ativo' and (self.data_expiracao is None or self.data_expiracao > datetime.utcnow())
    
    def can_access_feature(self, feature):
        permissoes = {
            'gratuito': ['busca_basica', 'visualizacao_limitada'],
            'basico': ['busca_basica', 'visualizacao_completa', 'exportar_pdf', '10_alertas'],
            'profissional': ['busca_avancada', 'visualizacao_completa', 'exportar_pdf', 'exportar_excel', 'precificacao_ia', '50_alertas', 'api_acesso'],
            'empresarial': ['tudo_ilimitado', 'multi_usuarios', 'relatorios_customizados', 'suporte_prioritario', 'api_completa']
        }
        return feature in permissoes.get(self.plano, [])

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(100))
    stripe_subscription_id = db.Column(db.String(100))
    valor = db.Column(db.Numeric(10, 2))
    moeda = db.Column(db.String(3), default='BRL')
    status = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_confirmacao = db.Column(db.DateTime)
    descricao = db.Column(db.String(255))
    fatura_url = db.Column(db.String(500))

class LogAcesso(db.Model):
    __tablename__ = 'logs_acesso'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    acao = db.Column(db.String(50))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    detalhes = db.Column(db.JSON)

# ==========================================
# CONFIGURAÇÃO DE PLANOS E PREÇOS
# ==========================================

PLANOS = {
    'gratuito': {
        'nome': 'Gratuito',
        'preco': 0,
        'descricao': 'Ideal para testar a plataforma',
        'features': [
            '10 consultas/mês',
            'Busca básica',
            'Visualização limitada',
            'Suporte por email'
        ],
        'stripe_price_id': None
    },
    'basico': {
        'nome': 'Básico',
        'preco': 97.00,
        'descricao': 'Para profissionais iniciantes',
        'features': [
            '100 consultas/mês',
            'Busca avançada',
            'Visualização completa',
            'Exportar PDF',
            '10 alertas personalizados',
            'Suporte prioritário'
        ],
        'stripe_price_id': 'price_basico'
    },
    'profissional': {
        'nome': 'Profissional',
        'preco': 297.00,
        'descricao': 'Para empresas que licitam regularmente',
        'features': [
            'Consultas ilimitadas',
            'Precificação com IA',
            'Exportar PDF e Excel',
            '50 alertas personalizados',
            'Acesso à API',
            'Suporte VIP',
            'Relatórios mensais'
        ],
        'stripe_price_id': 'price_profissional'
    },
    'empresarial': {
        'nome': 'Empresarial',
        'preco': 997.00,
        'descricao': 'Para grandes empresas e órgãos públicos',
        'features': [
            'Tudo ilimitado',
            'Multi-usuários (até 10)',
            'Relatórios customizados',
            'API completa',
            'Suporte dedicado',
            'Treinamento incluso',
            'SLA garantido'
        ],
        'stripe_price_id': 'price_empresarial'
    }
}

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def registrar_log(user_id, acao, detalhes=None):
    log = LogAcesso(
        user_id=user_id,
        acao=acao,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        detalhes=detalhes
    )
    db.session.add(log)
    db.session.commit()

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================
# ROTAS PÚBLICAS
# ==========================================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html', planos=PLANOS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        lembrar = request.form.get('lembrar') == 'on'
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if user.status_assinatura == 'suspenso':
                flash('Sua conta está suspensa. Entre em contato com o suporte.', 'error')
                return redirect(url_for('login'))
            
            login_user(user, remember=lembrar, duration=timedelta(days=30) if lembrar else None)
            user.data_ultimo_acesso = datetime.utcnow()
            db.session.commit()
            
            registrar_log(user.id, 'login')
            
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html', planos=PLANOS)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        nome = request.form.get('nome')
        empresa = request.form.get('empresa')
        cnpj = request.form.get('cnpj')
        telefone = request.form.get('telefone')
        plano = request.form.get('plano', 'gratuito')
        
        if User.query.filter_by(email=email).first():
            flash('Este email já está cadastrado.', 'error')
            return redirect(url_for('registro'))
        
        if len(password) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'error')
            return redirect(url_for('registro'))
        
        novo_usuario = User(
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            nome=nome,
            empresa=empresa,
            cnpj=cnpj,
            telefone=telefone,
            plano=plano,
            limite_consultas=10 if plano == 'gratuito' else 999999
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        if plano != 'gratuito':
            login_user(novo_usuario)
            return redirect(url_for('checkout', plano=plano))
        
        flash('Conta criada com sucesso! Faça login para começar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html', planos=PLANOS)

@app.route('/planos')
def planos():
    return render_template('planos.html', planos=PLANOS, stripe_key=STRIPE_PUBLIC_KEY)

@app.route('/logout')
@login_required
def logout():
    registrar_log(current_user.id, 'logout')
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))

# ==========================================
# ROTAS DO CLIENTE
# ==========================================

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.has_active_subscription():
        flash('Sua assinatura expirou. Renove para continuar usando.', 'warning')
        return redirect(url_for('planos'))
    
    estatisticas = {
        'consultas_restantes': max(0, current_user.limite_consultas - current_user.licitacoes_consultadas),
        'total_consultas': current_user.licitacoes_consultadas,
        'plano_nome': PLANOS[current_user.plano]['nome'],
        'data_expiracao': current_user.data_expiracao
    }
    
    return render_template('dashboard.html',
                         user=current_user, 
                         estatisticas=estatisticas,
                         planos=PLANOS)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    plano_id = request.args.get('plano') or request.form.get('plano')
    
    if not plano_id or plano_id not in PLANOS:
        return redirect(url_for('planos'))
    
    plano = PLANOS[plano_id]
    
    if plano['preco'] == 0:
        current_user.plano = plano_id
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            if not current_user.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=current_user.email,
                    name=current_user.nome,
                    metadata={'user_id': current_user.id, 'plano': plano_id}
                )
                current_user.stripe_customer_id = customer.id
                db.session.commit()
            
            checkout_session = stripe.checkout.Session.create(
                customer=current_user.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': f'LICITA AI PRO - Plano {plano["nome"]}',
                            'description': plano['descricao'],
                        },
                        'unit_amount': int(plano['preco'] * 100),
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=url_for('pagamento_sucesso', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('checkout', plano=plano_id, _external=True),
            )
            
            return redirect(checkout_session.url, code=303)
            
        except Exception as e:
            flash(f'Erro ao processar pagamento: {str(e)}', 'error')
            return redirect(url_for('checkout', plano=plano_id))
    
    return render_template('checkout.html', 
                         plano=plano, 
                         plano_id=plano_id,
                         user=current_user,
                         stripe_key=STRIPE_PUBLIC_KEY)

@app.route('/pagamento/sucesso')
@login_required
def pagamento_sucesso():
    session_id = request.args.get('session_id')
    
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            subscription = stripe.Subscription.retrieve(session.subscription)
            
            current_user.stripe_subscription_id = subscription.id
            current_user.status_assinatura = 'ativo'
            current_user.data_expiracao = datetime.fromtimestamp(subscription.current_period_end)
            
            if current_user.plano == 'basico':
                current_user.limite_consultas = 100
            elif current_user.plano in ['profissional', 'empresarial']:
                current_user.limite_consultas = 999999
            
            db.session.commit()
            
            pagamento = Pagamento(
                user_id=current_user.id,
                stripe_payment_intent_id=session.payment_intent,
                stripe_subscription_id=subscription.id,
                valor=session.amount_total / 100,
                status='pago',
                data_confirmacao=datetime.utcnow(),
                descricao=f'Assinatura {PLANOS[current_user.plano]["nome"]}'
            )
            db.session.add(pagamento)
            db.session.commit()
            
            registrar_log(current_user.id, 'pagamento_confirmado', {'plano': current_user.plano, 'valor': session.amount_total / 100})
            
            flash('Pagamento confirmado! Bem-vindo ao LICITA AI PRO.', 'success')
            
        except Exception as e:
            flash(f'Erro ao confirmar pagamento: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/minha-conta')
@login_required
def minha_conta():
    pagamentos = Pagamento.query.filter_by(user_id=current_user.id).order_by(Pagamento.data_criacao.desc()).all()
    logs = LogAcesso.query.filter_by(user_id=current_user.id).order_by(LogAcesso.data_hora.desc()).limit(50).all()
    
    return render_template('minha_conta.html', 
                         user=current_user, 
                         pagamentos=pagamentos, 
                         logs=logs,
                         planos=PLANOS)

@app.route('/api/verificar-acesso')
@login_required
def verificar_acesso():
    return jsonify({
        'plano': current_user.plano,
        'status': current_user.status_assinatura,
        'consultas_restantes': max(0, current_user.limite_consultas - current_user.licitacoes_consultadas),
        'tem_acesso': current_user.has_active_subscription()
    })

# ==========================================
# ROTAS ADMINISTRATIVAS
# ==========================================

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Acesso negado.', 'error')
        return redirect(url_for('dashboard'))
    
    total_usuarios = User.query.count()
    usuarios_ativos = User.query.filter_by(status_assinatura='ativo').count()
    usuarios_pendentes = User.query.filter_by(status_assinatura='pendente').count()
    
    usuarios_por_plano = db.session.query(
        User.plano, 
        db.func.count(User.id)
    ).group_by(User.plano).all()
    
    receita_mensal = db.session.query(
        db.func.sum(Pagamento.valor)
    ).filter(
        Pagamento.status == 'pago',
        Pagamento.data_confirmacao >= datetime.utcnow() - timedelta(days=30)
    ).scalar() or 0
    
    ultimos_usuarios = User.query.order_by(User.data_registro.desc()).limit(10).all()
    ultimos_pagamentos = Pagamento.query.filter_by(status='pago').order_by(Pagamento.data_confirmacao.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_usuarios=total_usuarios,
                         usuarios_ativos=usuarios_ativos,
                         usuarios_pendentes=usuarios_pendentes,
                         usuarios_por_plano=dict(usuarios_por_plano),
                         receita_mensal=receita_mensal,
                         ultimos_usuarios=ultimos_usuarios,
                         ultimos_pagamentos=ultimos_pagamentos,
                         planos=PLANOS)

@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    if not current_user.is_admin():
        return redirect(url_for('dashboard'))
    
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 50
    
    filtro_plano = request.args.get('plano', '')
    filtro_status = request.args.get('status', '')
    busca = request.args.get('busca', '')
    
    query = User.query
    
    if filtro_plano:
        query = query.filter_by(plano=filtro_plano)
    if filtro_status:
        query = query.filter_by(status_assinatura=filtro_status)
    if busca:
        query = query.filter(
            db.or_(
                User.email.contains(busca),
                User.nome.contains(busca),
                User.empresa.contains(busca)
            )
        )
    
    usuarios = query.order_by(User.data_registro.desc()).paginate(
        page=pagina, per_page=por_pagina, error_out=False
    )
    
    return render_template('admin_usuarios.html',
                         usuarios=usuarios,
                         planos=PLANOS,
                         filtros={'plano': filtro_plano, 'status': filtro_status, 'busca': busca})

@app.route('/admin/usuario/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_editar_usuario(id):
    if not current_user.is_superadmin():
        flash('Acesso negado. Apenas superadministradores.', 'error')
        return redirect(url_for('admin_usuarios'))
    
    usuario = User.query.get_or_404(id)
    
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.empresa = request.form.get('empresa')
        usuario.tipo = request.form.get('tipo')
        usuario.plano = request.form.get('plano')
        usuario.status_assinatura = request.form.get('status_assinatura')
        usuario.limite_consultas = request.form.get('limite_consultas', type=int)
        
        if request.form.get('data_expiracao'):
            usuario.data_expiracao = datetime.fromisoformat(request.form.get('data_expiracao'))
        
        db.session.commit()
        flash('Usuário atualizado com sucesso.', 'success')
        return redirect(url_for('admin_usuarios'))
    
    return render_template('admin_editar_usuario.html', usuario=usuario, planos=PLANOS)

@app.route('/admin/financeiro')
@login_required
def admin_financeiro():
    if not current_user.is_admin():
        return redirect(url_for('dashboard'))
    
    receita_por_mes = db.session.query(
        db.func.strftime('%Y-%m', Pagamento.data_confirmacao),
        db.func.sum(Pagamento.valor)
    ).filter(
        Pagamento.status == 'pago'
    ).group_by(
        db.func.strftime('%Y-%m', Pagamento.data_confirmacao)
    ).order_by(
        db.func.strftime('%Y-%m', Pagamento.data_confirmacao).desc()
    ).limit(12).all()
    
    receita_por_plano = db.session.query(
        User.plano,
        db.func.sum(Pagamento.valor)
    ).join(Pagamento).filter(
        Pagamento.status == 'pago'
    ).group_by(User.plano).all()
    
    return render_template('admin_financeiro.html',
                         receita_por_mes=receita_por_mes,
                         receita_por_plano=dict(receita_por_plano))

# ==========================================
# WEBHOOKS E APIs
# ==========================================

@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
    
    if event['type'] == 'invoice.payment_succeeded':
        subscription = event['data']['object']
        user = User.query.filter_by(stripe_subscription_id=subscription['id']).first()
        if user:
            user.status_assinatura = 'ativo'
            user.data_expiracao = datetime.fromtimestamp(subscription['current_period_end'])
            db.session.commit()
    
    elif event['type'] == 'invoice.payment_failed':
        subscription = event['data']['object']
        user = User.query.filter_by(stripe_subscription_id=subscription['id']).first()
        if user:
            user.status_assinatura = 'pendente'
            db.session.commit()
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        user = User.query.filter_by(stripe_subscription_id=subscription['id']).first()
        if user:
            user.status_assinatura = 'cancelado'
            user.plano = 'gratuito'
            user.limite_consultas = 10
            db.session.commit()
    
    return 'OK', 200

@app.route('/api/licitacoes')
@login_required
def api_licitacoes():
    if current_user.licitacoes_consultadas >= current_user.limite_consultas:
        return jsonify({
            'error': 'Limite de consultas atingido',
            'mensagem': 'Faça upgrade do seu plano para continuar consultando.'
        }), 429
    
    current_user.licitacoes_consultadas += 1
    db.session.commit()
    
    # Dados simulados de licitações
    dados = [
        {'id': 1, 'orgao': 'MEC', 'objeto': 'Computadores', 'valor': 50000, 'data': '2024-01-15'},
        {'id': 2, 'orgao': 'MS', 'objeto': 'Medicamentos', 'valor': 75000, 'data': '2024-01-20'}
    ]
    
    registrar_log(current_user.id, 'consulta_licitacao', {
        'resultados': len(dados),
        'consultas_restantes': current_user.limite_consultas - current_user.licitacoes_consultadas
    })
    
    return jsonify(dados)

# ==========================================
# INICIALIZAÇÃO
# ==========================================

def criar_usuario_admin():
    """Cria usuário admin inicial se não existir"""
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(email='admin@licitai.pro').first():
            admin = User(
                email='admin@licitai.pro',
                password_hash=generate_password_hash('Admin@123', method='pbkdf2:sha256'),
                nome='Administrador',
                tipo='superadmin',
                plano='empresarial',
                status_assinatura='ativo',
                limite_consultas=999999
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Usuário admin criado: admin@licitai.pro / Admin@123')

if __name__ == '__main__':
    criar_usuario_admin()
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Quando executado pelo Gunicorn (Render)
    criar_usuario_admin()