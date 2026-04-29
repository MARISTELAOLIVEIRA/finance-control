from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os

# Inicializa Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_control.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa banco de dados
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== MODELOS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(11))
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    transacoes = db.relationship('Transacao', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, senha):
        self.senha = generate_password_hash(senha)
    
    def check_password(self, senha):
        return check_password_hash(self.senha, senha)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'
    categoria = db.Column(db.String(50), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email', '').strip()
        senha = data.get('senha', '')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(senha):
            login_user(user)
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            return redirect(url_for('dashboard'))
        
        if request.is_json:
            return jsonify({'success': False, 'error': 'E-mail ou senha inválidos'}), 401
        
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        nome = data.get('nome', '').strip()
        email = data.get('email', '').strip()
        cpf = data.get('cpf', '').strip()
        telefone = data.get('telefone', '').strip()
        senha = data.get('senha', '')
        confirmar_senha = data.get('confirmar_senha', '')
        
        # Validações
        if not all([nome, email, cpf, senha]):
            return jsonify({'success': False, 'error': 'Preencha todos os campos obrigatórios'}), 400
        
        if len(senha) < 6:
            return jsonify({'success': False, 'error': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        if senha != confirmar_senha:
            return jsonify({'success': False, 'error': 'As senhas não correspondem'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'E-mail já registrado'}), 400
        
        if User.query.filter_by(cpf=cpf).first():
            return jsonify({'success': False, 'error': 'CPF já registrado'}), 400
        
        # Cria novo usuário
        novo_usuario = User(nome=nome, email=email, cpf=cpf, telefone=telefone)
        novo_usuario.set_password(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'redirect': url_for('login')})
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ==================== ROTAS DO DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    # Calcula resumo financeiro
    transacoes = Transacao.query.filter_by(usuario_id=current_user.id).all()
    
    receitas_mes = sum(t.valor for t in transacoes 
                       if t.tipo == 'receita' and t.data.month == mes_atual and t.data.year == ano_atual)
    despesas_mes = sum(t.valor for t in transacoes 
                       if t.tipo == 'despesa' and t.data.month == mes_atual and t.data.year == ano_atual)
    
    saldo_atual = receitas_mes - despesas_mes
    economia = saldo_atual
    
    # Últimas transações
    ultimas_transacoes = Transacao.query.filter_by(usuario_id=current_user.id).order_by(
        Transacao.data.desc()).limit(10).all()
    
    return render_template('dashboard.html',
                         saldo_atual=saldo_atual,
                         receitas_mes=receitas_mes,
                         despesas_mes=despesas_mes,
                         economia=economia,
                         transacoes=ultimas_transacoes,
                         mes_ano=f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][mes_atual-1]} de {ano_atual}")


# ==================== API DE TRANSAÇÕES ====================

@app.route('/api/transacoes', methods=['GET'])
@login_required
def get_transacoes():
    transacoes = Transacao.query.filter_by(usuario_id=current_user.id).order_by(
        Transacao.data.desc()).all()
    
    return jsonify([{
        'id': t.id,
        'descricao': t.descricao,
        'valor': t.valor,
        'tipo': t.tipo,
        'categoria': t.categoria,
        'data': t.data.strftime('%d/%m/%Y %H:%M')
    } for t in transacoes])


@app.route('/api/transacoes', methods=['POST'])
@login_required
def criar_transacao():
    data = request.get_json()
    
    # Validações
    if not all(k in data for k in ['descricao', 'valor', 'tipo', 'categoria']):
        return jsonify({'success': False, 'error': 'Campos obrigatórios faltando'}), 400
    
    try:
        valor = float(data['valor'])
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
    except ValueError:
        return jsonify({'success': False, 'error': 'Valor inválido'}), 400
    
    if data['tipo'] not in ['receita', 'despesa']:
        return jsonify({'success': False, 'error': 'Tipo inválido'}), 400
    
    # Cria nova transação
    transacao = Transacao(
        usuario_id=current_user.id,
        descricao=data['descricao'],
        valor=valor,
        tipo=data['tipo'],
        categoria=data['categoria']
    )
    
    db.session.add(transacao)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'transacao': {
            'id': transacao.id,
            'descricao': transacao.descricao,
            'valor': transacao.valor,
            'tipo': transacao.tipo,
            'categoria': transacao.categoria,
            'data': transacao.data.strftime('%d/%m/%Y %H:%M')
        }
    }), 201


@app.route('/api/transacoes/<int:transacao_id>', methods=['DELETE'])
@login_required
def deletar_transacao(transacao_id):
    transacao = Transacao.query.get_or_404(transacao_id)
    
    # Verifica se a transação pertence ao usuário
    if transacao.usuario_id != current_user.id:
        return jsonify({'success': False, 'error': 'Não autorizado'}), 403
    
    db.session.delete(transacao)
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/relatorio')
@login_required
def relatorio():
    """Retorna relatório financeiro do mês"""
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    transacoes = Transacao.query.filter_by(usuario_id=current_user.id).all()
    
    # Filtra transações do mês
    transacoes_mes = [t for t in transacoes 
                      if t.data.month == mes_atual and t.data.year == ano_atual]
    
    # Agrupa por categoria
    categorias = {}
    for t in transacoes_mes:
        if t.categoria not in categorias:
            categorias[t.categoria] = {'receita': 0, 'despesa': 0}
        categorias[t.categoria][t.tipo] += t.valor
    
    return jsonify({
        'mês': f"{['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][mes_atual-1]}/{ano_atual}",
        'categorias': categorias,
        'total_receitas': sum(t.valor for t in transacoes_mes if t.tipo == 'receita'),
        'total_despesas': sum(t.valor for t in transacoes_mes if t.tipo == 'despesa')
    })


# ==================== ERRO HANDLING ====================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('erro_404.html'), 404


@app.errorhandler(500)
def erro_servidor(erro):
    db.session.rollback()
    return render_template('erro_500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
