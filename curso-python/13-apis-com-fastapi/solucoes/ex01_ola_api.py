"""
Exercício 13.01 — Olá, API! (SOLUÇÃO)
"""

from fastapi import FastAPI

VERSAO = "1.0.0"

app = FastAPI()


# O decorador "registra" a função no app: quando chegar um GET em "/", o
# FastAPI chama raiz() e converte o dicionário devolvido em JSON.
@app.get("/")
def raiz() -> dict:
    return {"mensagem": "API do laboratório no ar"}


@app.get("/saude")
def saude() -> dict:
    return {"status": "ok"}


@app.get("/versao")
def versao() -> dict:
    # Usar a constante evita duas "verdades" diferentes no código: quando a
    # versão mudar, você muda num lugar só.
    return {"versao": VERSAO}


# Alternativa que você vai ver muito por aí: passar a versão para o próprio app,
# FastAPI(version=VERSAO). Ela aparece no /docs e no /openapi.json.
