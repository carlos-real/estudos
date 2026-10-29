"""
Exercício 13.01 — Olá, API!
Nível: ★☆☆

Contexto: antes de qualquer regra de negócio, toda API tem rotas simples que
dizem "estou no ar" e "qual versão está rodando". O monitoramento da TI e
outros sistemas consultam essas rotas o dia todo.

Tarefa: no `app` abaixo, crie três rotas GET:
- "/"        devolve {"mensagem": "API do laboratório no ar"}
- "/saude"   devolve {"status": "ok"}
- "/versao"  devolve {"versao": VERSAO}   (use a constante, não escreva "1.0.0")

Exemplos:
    >>> from fastapi.testclient import TestClient
    >>> cliente = TestClient(app)
    >>> cliente.get("/saude").json()
    {'status': 'ok'}
    >>> cliente.get("/versao").status_code
    200

Dica: cada rota é uma função comum com o decorador @app.get("/caminho") em
cima. A função devolve um dicionário; o FastAPI transforma em JSON.

Teste com:  python curso.py testar 13 ex01
"""

from fastapi import FastAPI

VERSAO = "1.0.0"

app = FastAPI()

# Escreva suas rotas aqui (uma função com @app.get(...) para cada uma)
