"""
Exercício 13.11 — Revisão: API de medições com SQLite e estatística
Nível: ★★★

Revisão de: SQLite com parâmetros "?" e row_factory (módulo 11), statistics
(módulo 07), dicionários e agrupamento (módulo 03) + FastAPI (este módulo).

Contexto: o laboratório quer lançar medições pela API e ver, por OP, o resumo
estatístico de cada ensaio (n, média, desvio padrão, mínimo e máximo), como
no relatório de série. Os dados precisam sobreviver ao reinício: SQLite.

Tarefa:
1. criar_tabela(con): cria (se não existir) a tabela
       medicoes (id INTEGER PRIMARY KEY AUTOINCREMENT, op TEXT NOT NULL,
                 ensaio TEXT NOT NULL, valor REAL NOT NULL)
2. obter_conexao(): dependência com yield. Conecta em CAMINHO_BANCO com
   check_same_thread=False, define row_factory = sqlite3.Row, chama
   criar_tabela, entrega a conexão (yield) e a FECHA no fim (finally).
3. MedicaoEntrada: op (6 dígitos), ensaio (mínimo 2 caracteres), valor (> 0).
4. Rotas (recebendo a conexão por Depends(obter_conexao)):
   - POST /medicoes -> 201, grava e devolve {"id", "op", "ensaio", "valor"}.
   - GET /ops/{op}/resumo -> {"op": op, "ensaios": {...}}, um item por ensaio
     em ordem alfabética:
         {"n": 3, "media": 20.1, "desvio": 0.3, "minimo": 19.8, "maximo": 20.4}
     media e desvio arredondados com round(..., 3). desvio = statistics.stdev
     quando n >= 2, e 0.0 quando n == 1.
     OP sem medições -> 404 com detail "OP X sem medições".

Exemplos:
    >>> cliente.post("/medicoes", json={"op": "123456", "ensaio": "cof", "valor": 0.25}).json()
    {'id': 1, 'op': '123456', 'ensaio': 'cof', 'valor': 0.25}
    >>> cliente.get("/ops/123456/resumo").json()
    {'op': '123456', 'ensaios': {'cof': {'n': 1, 'media': 0.25, 'desvio': 0.0,
     'minimo': 0.25, 'maximo': 0.25}}}

Dica: nos testes, obter_conexao é trocada por uma conexão em memória
(app.dependency_overrides). Por isso as rotas devem usar SÓ a conexão que
recebem. Para o resumo: SELECT ensaio, valor ... WHERE op = ? ORDER BY ensaio,
depois agrupe os valores num dicionário {ensaio: [valores]}.

Teste com:  python curso.py testar 13 ex11
"""

import sqlite3
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

CAMINHO_BANCO = Path(__file__).resolve().parent / "medicoes_ex11.db"


def criar_tabela(con: sqlite3.Connection) -> None:
    """Cria a tabela medicoes, se ainda não existir."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def obter_conexao():
    """Dependência: abre a conexão, entrega com yield e fecha no fim."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


class MedicaoEntrada(BaseModel):
    """Corpo do POST. Campos: op, ensaio, valor."""

    # Escreva seus campos aqui


app = FastAPI()

# Escreva suas rotas aqui
