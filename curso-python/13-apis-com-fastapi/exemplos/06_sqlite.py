"""Exemplo 06 — Persistência com SQLite: os dados sobrevivem ao reinício.

O banco fica em exemplos/saida/medicoes.db. A conexão chega às rotas por uma
dependência com yield (abre antes, fecha depois de cada requisição).

Rode com:
    python exemplos/06_sqlite.py             # demonstração (recria o banco)
    python exemplos/06_sqlite.py --servir
"""

import sqlite3
import sys
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

CAMINHO_BANCO = Path(__file__).resolve().parent / "saida" / "medicoes.db"

app = FastAPI(title="Medições (SQLite)")


class MedicaoEntrada(BaseModel):
    op: str = Field(pattern=r"^\d{6}$")
    ensaio: str = Field(min_length=2)
    valor: float = Field(gt=0)


class Medicao(MedicaoEntrada):
    id: int


def criar_tabela(con: sqlite3.Connection) -> None:
    con.execute(
        """CREATE TABLE IF NOT EXISTS medicoes (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               op TEXT NOT NULL,
               ensaio TEXT NOT NULL,
               valor REAL NOT NULL)"""
    )


def obter_conexao():
    """Dependência com yield: o código antes do yield roda ANTES da rota, o do
    finally roda DEPOIS (mesmo se a rota der erro)."""
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    # check_same_thread=False: o FastAPI pode usar a conexão em outra thread.
    con = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False)
    con.row_factory = sqlite3.Row  # linhas que funcionam como dicionário
    try:
        criar_tabela(con)
        yield con
    finally:
        con.close()


Conexao = Annotated[sqlite3.Connection, Depends(obter_conexao)]


@app.post("/medicoes", status_code=status.HTTP_201_CREATED)
def criar_medicao(entrada: MedicaoEntrada, con: Conexao) -> Medicao:
    with con:  # transação: commit se tudo der certo, rollback se der erro
        cursor = con.execute(
            "INSERT INTO medicoes (op, ensaio, valor) VALUES (?, ?, ?)",
            (entrada.op, entrada.ensaio, entrada.valor),
        )
    return Medicao(id=cursor.lastrowid, **entrada.model_dump())


@app.get("/medicoes")
def listar_medicoes(con: Conexao, op: str | None = None) -> list[Medicao]:
    if op is None:
        linhas = con.execute("SELECT * FROM medicoes ORDER BY id").fetchall()
    else:
        linhas = con.execute(
            "SELECT * FROM medicoes WHERE op = ? ORDER BY id", (op,)
        ).fetchall()
    return [Medicao(**dict(linha)) for linha in linhas]


@app.get("/medicoes/{id_medicao}")
def ver_medicao(id_medicao: int, con: Conexao) -> Medicao:
    linha = con.execute("SELECT * FROM medicoes WHERE id = ?", (id_medicao,)).fetchone()
    if linha is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Medição não encontrada")
    return Medicao(**dict(linha))


def demonstrar() -> None:
    CAMINHO_BANCO.unlink(missing_ok=True)  # começa do zero a cada demonstração
    cliente = TestClient(app)
    for corpo in [
        {"op": "123456", "ensaio": "espessura", "valor": 20.4},
        {"op": "123456", "ensaio": "cof", "valor": 0.27},
        {"op": "123789", "ensaio": "espessura", "valor": 39.8},
    ]:
        resposta = cliente.post("/medicoes", json=corpo)
        print("POST ->", resposta.status_code, resposta.json())

    print("GET /medicoes?op=123456 ->", cliente.get("/medicoes", params={"op": "123456"}).json())

    # "Reiniciar o servidor": um cliente novo, mas o arquivo do banco continua lá.
    outro_cliente = TestClient(app)
    print("Depois do reinício, /medicoes/3 ->", outro_cliente.get("/medicoes/3").json())
    print("GET /medicoes/99 ->", outro_cliente.get("/medicoes/99").status_code)


if __name__ == "__main__":
    if "--servir" in sys.argv:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        demonstrar()
