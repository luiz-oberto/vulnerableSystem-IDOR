# Demo IDOR — Boletim de Notas (Flask + SQLite)

Este projeto demonstra a vulnerabilidade **IDOR** usando a temática de boletim escolar.
Ele possui uma rota **vulnerável** (`/notas/<aluno_id>`) e uma rota **segura** (`/minhas-notas`).

## Como rodar

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Inicializar banco e dados de exemplo
python db_init.py

# Executar app (modo vulnerável por padrão)
python app.py
# Abra http://127.0.0.1:5000

# Usuários de exemplo:
#  - alice / alice
#  - bob   / bob
```
### Alternar entre modo VULNERÁVEL e SEGURO
Abra `app.py` e ajuste `app.config["VULNERABLE"]` para `True` (vulnerável) ou `False` (seguro).
No modo **seguro**, a rota `/notas/<aluno_id>` retorna 403 e a navegação recomenda `/minhas-notas`.
