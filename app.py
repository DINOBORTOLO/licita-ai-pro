from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
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
    # Local - usar arquivo SQLite
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'usuarios.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print(f"💻 Local: {db_path}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    data_ultimo_acesso = db.Column(db.DateTime)
    data_expiracao = db.Column(db.DateTime)
    
    licitacoes_consultadas = db.Column(db.Integer, default=0)
    limite_consultas = db.Column(db.Integer, default=10)
    
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
        ]
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
        ]
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
        ]
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
        ]
    }
}

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def registrar_log(user_id, acao, detalhes=None):
    try:
        log = LogAcesso(
            user_id=user_id,
            acao=acao,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            detalhes=detalhes or {}
        )
        db.session.add(log)
        db.session.commit()
    except:
        db.session.rollback()

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
        empresa = request.form.get('empresa', '')
        cnpj = request.form.get('cnpj', '')
        telefone = request.form.get('telefone', '')
        plano = request.form.get('plano', 'gratuito')
        
        # Verificar se email já existe
        if User.query.filter_by(email=email).first():
            flash('Este email já está cadastrado.', 'error')
            return redirect(url_for('registro'))
        
        # Validar senha
        if len(password) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'error')
            return redirect(url_for('registro'))
        
        # Criar novo usuário
        novo_usuario = User(
            email=email,
            password_hash=generate_password_hash(password),
            nome=nome,
            empresa=empresa,
            cnpj=cnpj,
            telefone=telefone,
            plano=plano,
            limite_consultas=10 if plano == 'gratuito' else 999999
        )
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            
            if plano != 'gratuito':
                login_user(novo_usuario)
                return redirect(url_for('checkout', plano=plano))
            
            flash('Conta criada com sucesso! Faça login para começar.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar conta: {str(e)}', 'error')
            return redirect(url_for('registro'))
    
    return render_template('registro.html', planos=PLANOS)

@app.route('/planos')
def planos():
    return render_template('planos.html', planos=PLANOS)

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

@app.route('/checkout/<plano>')
@login_required
def checkout(plano):
    if plano not in PLANOS:
        return redirect(url_for('planos'))
    
    return render_template('checkout.html', 
                         plano=PLANOS[plano], 
                         plano_id=plano,
                         user=current_user)

@app.route('/pagamento/sucesso')
@login_required
def pagamento_sucesso():
    flash('Pagamento confirmado! Bem-vindo ao LICITA AI PRO.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/minha-conta')
@login_required
def minha_conta():
    return render_template('minha_conta.html', 
                         user=current_user, 
                         planos=PLANOS)

# ==========================================
# API DE LICITAÇÕES
# ==========================================

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
        {'id': 861, 'orgao': 'Ministério da Educação - MEC', 'objeto': 'Aquisição de equipamentos de informática para laboratórios', 'valor': 2263830.50, 'data': '2026-03-12'},
        {'id': 860, 'orgao': 'INCRA - Instituto Nacional de Colonização', 'objeto': 'Contratação de serviços de consultoria técnica especializada', 'valor': 805691.25, 'data': '2026-03-11'},
        {'id': 859, 'orgao': 'UFPE - Universidade Federal de Pernambuco', 'objeto': 'Fornecimento de material de construção civil para obras', 'valor': 444650.00, 'data': '2026-03-10'}
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
    try:
        if not User.query.filter_by(email='admin@licitai.pro').first():
            admin = User(
                email='admin@licitai.pro',
                password_hash=generate_password_hash('Admin@123'),
                nome='Administrador',
                tipo='superadmin',
                plano='empresarial',
                status_assinatura='ativo',
                limite_consultas=999999
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Usuário admin criado: admin@licitai.pro / Admin@123')
    except Exception as e:
        print(f'⚠️ Erro ao criar admin: {e}')
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        criar_usuario_admin()
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Para o Gunicorn (Render)
    with app.app_context():
        db.create_all()
        criar_usuario_admin()