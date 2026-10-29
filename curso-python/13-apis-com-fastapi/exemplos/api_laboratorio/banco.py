"""Acesso ao SQLite: caminho do banco, criação das tabelas e dependência de conexão."""

import os
import sqlite3
from pathlib import Path
from typing import Annotated

from fastapi import Depends

CAMINHO_PADRAO = Path(__file__).resolve().parent.parent / "saida" / "api_laboratorio.db"

# linha, ensaio, tipo, minimo, maximo, nominal, percentual
TOLERANCIAS_INICIAIS = [
    ("A", "espessura", "nominal", None, None, 20.0, 10.0),
    ("A", "cof", "faixa", 0.20, 0.30, None, None),
    ("B", "espessura", "nominal", None, None, 40.0, 5.0),
    ("B", "gramatura", "nominal", None, None, 38.0, 4.0),
    ("C", "tracao", "faixa", 25.0, 40.0, None, None),
    ("D", "selagem", "faixa", 1.5, 3.0, None, None),
]

ESQUEMA = """
CREATE TABLE IF NOT EXISTS tolerancias (
    linha TEXT NOT NULL,
    ensaio TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('faixa', 'nominal')),
    minimo REAL,
    maximo REAL,
    nominal REAL,
    percentual REAL,
    PRIMARY KEY (linha, ensaio)
);
CREATE TABLE IF NOT EXISTS medicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    op TEXT NOT NULL,
    linha TEXT NOT NULL,
    ensaio TEXT NOT NULL,
    valor REAL NOT NULL,
    aprovado INTEGER NOT NULL
);
"""


def caminho_banco() -> Path:
    """A variável de ambiente API_LAB_BANCO permite trocar o banco sem mexer no código."""
    return Path(os.environ.get("API_LAB_BANCO", CAMINHO_PADRAO))


def preparar(con: sqlite3.Connection) -> None:
    con.executescript(ESQUEMA)
    vazio = con.execute("SELECT COUNT(*) FROM tolerancias").fetchone()[0] == 0
    if vazio:
        with con:
            con.executemany(
                "INSERT INTO tolerancias VALUES (?, ?, ?, ?, ?, ?, ?)", TOLERANCIAS_INICIAIS
            )


def obter_conexao():
    caminho = caminho_banco()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(caminho, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        preparar(con)
        yield con
    finally:
        con.close()


Conexao = Annotated[sqlite3.Connection, Depends(obter_conexao)]
