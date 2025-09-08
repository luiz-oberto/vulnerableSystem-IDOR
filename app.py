from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Nota, AlunoInfo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'  # para demo
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boletim.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Toggle do modo vulnerável vs seguro
# True  -> rota /notas/<aluno_id> NÃO valida o usuário (IDOR presente)
# False -> rota /notas/<aluno_id> exige que aluno_id == session['user_id']
app.config['VULNERABLE'] = True

# página inicial
app.config['START_PAGE'] = 'notas'

db.init_app(app)

def login_required(view):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.path))
        return view(*args, **kwargs)
    wrapper.__name__ = view.__name__
    return wrapper


@app.route('/')
@login_required
def index():
    target = app.config.get('START_PAGE', 'notas')
    if target == 'dados':
        return redirect(url_for('meus_dados'))
    # padrão: notas
    return redirect(url_for('notas_aluno', aluno_id=session['user_id']))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user, current_app=app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.password_plain == password:
            session['user_id'] = user.id
            flash('Login efetuado com sucesso.', 'success')
            next_url = request.args.get('next') or url_for('notas_aluno', aluno_id=session['user_id']) # index | 'notas_aluno', aluno_id=session['user_id']
            return redirect(next_url)
        flash('Credenciais inválidas.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('login'))

# ROTA VULNERÁVEL (ou segura se VULNERABLE=False)
@app.route('/notas/<int:aluno_id>')
@login_required
def notas_aluno(aluno_id):
    if not app.config['VULNERABLE']:
        # Modo seguro: só permite ver as próprias notas
        if session['user_id'] != aluno_id:
            abort(403)  # Proibido
    aluno = User.query.get_or_404(aluno_id)
    notas = Nota.query.filter_by(aluno_id=aluno_id).all()
    template = 'notas_vulneravel.html' if app.config['VULNERABLE'] else 'notas_seguro.html'
    return render_template(template, aluno=aluno, notas=notas)

# ROTA SEGURA RECOMENDADA
@app.route('/minhas-notas')
@login_required
def minhas_notas():
    aluno_id = session['user_id']
    aluno = User.query.get_or_404(aluno_id)
    notas = Nota.query.filter_by(aluno_id=aluno_id).all()
    return render_template('notas_seguro.html', aluno=aluno, notas=notas)

# --------- Dados Pessoais (IDOR explícito) ---------
@app.route('/dados/<int:aluno_id>')
@login_required
def dados_pessoais(aluno_id):
    # Se estiver no modo SEGURO, só permite ver os próprios dados
    if not app.config['VULNERABLE']:
        if session['user_id'] != aluno_id:
            abort(403)

    aluno = User.query.get_or_404(aluno_id)
    info = AlunoInfo.query.filter_by(aluno_id=aluno_id).first_or_404()

    # Use um template diferente para enfatizar a vulnerabilidade
    template = 'dados_vulneravel.html' if app.config['VULNERABLE'] else 'dados_seguro.html'
    return render_template(template, aluno=aluno, info=info)

@app.route('/meus-dados')
@login_required
def meus_dados():
    aluno_id = session['user_id']
    aluno = User.query.get_or_404(aluno_id)
    info = AlunoInfo.query.filter_by(aluno_id=aluno_id).first()
    if not info:
        flash('Sem dados pessoais cadastrados.', 'warning')
        return redirect(url_for('index'))
    return render_template('dados_seguro.html', aluno=aluno, info=info)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
