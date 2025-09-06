from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_plain = db.Column(db.String(50), nullable=False)  # apenas para demonstração DIDÁTICA

    def __repr__(self):
        return f'<User {self.username}>'

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    disciplina = db.Column(db.String(120), nullable=False)
    nota = db.Column(db.Float, nullable=False)

    aluno = db.relationship('User', backref='notas')

    def __repr__(self):
        return f'<Nota {self.disciplina}={self.nota} aluno={self.aluno_id}>'

class AlunoInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True, index=True)
    matricula = db.Column(db.String(30), nullable=False, unique=True)
    nome_pai = db.Column(db.String(120))
    nome_mae = db.Column(db.String(120))
    cpf = db.Column(db.String(14))  # formato fictício: 000.000.000-00
    telefone = db.Column(db.String(30))
    email_contato = db.Column(db.String(120))
    endereco = db.Column(db.String(255))

    aluno = db.relationship('User', backref='info_pessoal', uselist=False)

    def __repr__(self):
        return f'<AlunoInfo {self.matricula} aluno={self.aluno_id}>'
