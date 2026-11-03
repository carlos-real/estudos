"""Monta os bancos SQLite do módulo 11 a partir dos scripts .sql desta pasta.

Uso (na pasta curso-python):
    python 11-banco-de-dados-e-sql/dados/montar_banco.py

Cria (ou recria do zero):
    dados/laboratorio.db   o banco de exemplo da aula (OPs, ensaios, expedição)
    dados/regras.db        o banco de regras do projeto final

Abra os .db no DB Browser for SQLite (https://sqlitebrowser.org) para ver as
tabelas e testar consultas. Pode rodar quantas vezes quiser.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent


def montar(script: Path, destino: Path) -> Path:
    """Apaga o banco antigo e executa o script SQL num banco novo."""
    destino.unlink(missing_ok=True)
    conexao = sqlite3.connect(destino)
    try:
        # executescript roda VÁRIOS comandos SQL de uma vez (separados por ";").
        # Use só com scripts seus, nunca com texto vindo de usuário.
        conexao.executescript(script.read_text(encoding="utf-8"))
        conexao.commit()
    finally:
        conexao.close()
    return destino


if __name__ == "__main__":
    for nome in ("laboratorio", "regras"):
        caminho = montar(PASTA / f"{nome}.sql", PASTA / f"{nome}.db")
        print(f"Banco gerado: {caminho.name} ({caminho.stat().st_size / 1024:.0f} KB)")
