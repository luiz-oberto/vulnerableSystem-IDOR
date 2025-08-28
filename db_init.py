from flask import Flask
from models import db, User, Nota

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boletim.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    alice = User(username='alice', nome='Alice Santos', email='alice@example.com', password_plain='alice')
    bob   = User(username='bob',   nome='Bob Silva',    email='bob@example.com',   password_plain='bob')
    db.session.add_all([alice, bob])
    db.session.commit()

    notas = [
        Nota(aluno_id=alice.id, disciplina='Matemática', nota=9.2),
        Nota(aluno_id=alice.id, disciplina='Português',  nota=8.5),
        Nota(aluno_id=alice.id, disciplina='Física',     nota=7.8),
        Nota(aluno_id=bob.id,   disciplina='Matemática', nota=6.1),
        Nota(aluno_id=bob.id,   disciplina='Português',  nota=7.0),
        Nota(aluno_id=bob.id,   disciplina='História',   nota=8.9),
    ]
    db.session.add_all(notas)
    db.session.commit()
    print('Banco criado e populado com sucesso.')
