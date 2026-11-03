"""
Exercício 13.11 — Revisão: API de medições com SQLite e estatística (SOLUÇÃO)
"""

import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

CAMINHO_BANCO = Path(__file__).resolve().parent / "medicoes_ex11.db"


def criar_tabela(con: sqlite3.Connection) -> None:
    """Cria a tabela medicoes, se ainda não existir."""
    con.execute(
        """CREATE TABLE IF NOT EXISTS medicoes (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               op TEXT NOT NULL,
               ensaio TEXT NOT NULL,
               valor REAL NOT NULL)"""
    )


def obter_conexao():
    """Dependência: abre a conexão, entrega com yield e fecha no fim."""
    # check_same_thread=False: o FastAPI pode preparar a dependência numa
    # thread e rodar a rota em outra. Cada requisição tem a SUA conexão.
    con = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        criar_tabela(con)
        yield con
    finally:
        con.close()  # roda depois da resposta, mesmo se a rota der erro


class MedicaoEntrada(BaseModel):
    """Corpo do POST. Campos: op, ensaio, valor."""

    op: str = Field(pattern=r"^\d{6}$")
    ensaio: str = Field(min_length=2)
    valor: float = Field(gt=0)


Conexao = Annotated[sqlite3.Connection, Depends(obter_conexao)]

app = FastAPI()


@app.post("/medicoes", status_code=status.HTTP_201_CREATED)
def criar_medicao(entrada: MedicaoEntrada, con: Conexao) -> dict:
    with con:  # commit no fim do bloco (ou rollback se der erro) — módulo 11
        cursor = con.execute(
            # Parâmetros com "?": NUNCA monte SQL com f-string (SQL injection).
            "INSERT INTO medicoes (op, ensaio, valor) VALUES (?, ?, ?)",
            (entrada.op, entrada.ensaio, entrada.valor),
        )
    return {"id": cursor.lastrowid, **entrada.model_dump()}


def estatisticas(valores: list[float]) -> dict:
    """Resumo de uma série (módulo 07). Função pura: fácil de testar sozinha."""
    return {
        "n": len(valores),
        "media": round(statistics.mean(valores), 3),
        # stdev precisa de pelo menos 2 valores (senão StatisticsError).
        "desvio": round(statistics.stdev(valores), 3) if len(valores) >= 2 else 0.0,
        "minimo": min(valores),
        "maximo": max(valores),
    }


@app.get("/ops/{op}/resumo")
def resumo_da_op(op: str, con: Conexao) -> dict:
    linhas = con.execute(
        "SELECT ensaio, valor FROM medicoes WHERE op = ? ORDER BY ensaio, id", (op,)
    ).fetchall()
    if not linhas:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"OP {op} sem medições")

    por_ensaio: defaultdict[str, list[float]] = defaultdict(list)
    for linha in linhas:  # sqlite3.Row: acesso por nome de coluna
        por_ensaio[linha["ensaio"]].append(linha["valor"])

    # ORDER BY ensaio no SQL + dicionário que mantém a ordem de inserção
    # = ensaios em ordem alfabética na resposta.
    return {"op": op, "ensaios": {e: estatisticas(v) for e, v in por_ensaio.items()}}

    # Alternativa: deixar o SQL fazer parte do trabalho:
    #   SELECT ensaio, COUNT(*), AVG(valor), MIN(valor), MAX(valor)
    #   FROM medicoes WHERE op = ? GROUP BY ensaio ORDER BY ensaio
    # O SQLite não tem desvio padrão nativo, então o stdev continuaria no Python.
