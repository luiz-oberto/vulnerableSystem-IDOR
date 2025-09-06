# db_init.py
from flask import Flask
from models import db, User, Nota, AlunoInfo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boletim.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # (re)cria o banco do zero para a demo
    db.drop_all()
    db.create_all()

    # --- Usuários de exemplo ---
    alice = User(username='alice', nome='Alice Santos', email='alice@example.com', password_plain='alice')
    bob   = User(username='bob',   nome='Bob Silva',    email='bob@example.com',   password_plain='bob')
    db.session.add_all([alice, bob])
    db.session.commit()  # precisa do commit para termos os IDs

    # --- Notas de exemplo ---
    notas = [
        Nota(aluno_id=alice.id, disciplina='Matemática', nota=9.2),
        Nota(aluno_id=alice.id, disciplina='Português',  nota=8.5),
        Nota(aluno_id=alice.id, disciplina='Física',     nota=7.8),

        Nota(aluno_id=bob.id,   disciplina='Matemática', nota=6.1),
        Nota(aluno_id=bob.id,   disciplina='Português',  nota=7.0),
        Nota(aluno_id=bob.id,   disciplina='História',   nota=8.9),
    ]
    db.session.add_all(notas)

    # --- Dados pessoais (AlunoInfo) ---
    infos = [
        AlunoInfo(
            aluno_id=alice.id,
            matricula='A2025-001',
            nome_pai='Carlos Santos',
            nome_mae='Marina Santos',
            cpf='123.456.789-00',                 # fictício, para DEMO
            telefone='(11) 91234-5678',
            email_contato='alice.contato@example.com',
            endereco='Rua das Flores, 123 — São Paulo/SP'
        ),
        AlunoInfo(
            aluno_id=bob.id,
            matricula='A2025-002',
            nome_pai='Paulo Silva',
            nome_mae='Ana Silva',
            cpf='987.654.321-00',                 # fictício, para DEMO
            telefone='(21) 99876-5432',
            email_contato='bob.contato@example.com',
            endereco='Av. Central, 456 — Rio de Janeiro/RJ'
        ),
    ]
    db.session.add_all(infos)

    db.session.commit()
    print('Banco criado e populado com sucesso (usuários, notas e dados pessoais).')
