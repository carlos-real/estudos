"""
Exercício 13.02 — Parâmetros de caminho (SOLUÇÃO)
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/dobro/{numero}")
def dobro(numero: int) -> dict:
    # O type hint `int` não é enfeite: o FastAPI usa para converter "21" em 21
    # e para responder 422 quando o texto não é um inteiro. Sem ele, numero
    # chegaria como str e "21" * 2 daria "2121"!
    return {"numero": numero, "dobro": numero * 2}


@app.get("/saudacao/{nome}")
def saudacao(nome: str) -> dict:
    return {"mensagem": f"Olá, {nome}!"}
