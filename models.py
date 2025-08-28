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
