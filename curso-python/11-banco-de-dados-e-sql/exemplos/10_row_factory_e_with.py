"""Exemplo 10 — row_factory (linhas com nome de coluna) e fechar a conexão direito.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/10_row_factory_e_with.py
"""

import sqlite3
from contextlib import closing
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"

# closing(...) garante o close() no fim do bloco, mesmo se der erro.
with closing(sqlite3.connect(":memory:")) as conexao:
    conexao.executescript((DADOS / "laboratorio.sql").read_text(encoding="utf-8"))

    # Padrão: cada linha é uma tupla (acesso por posição)
    linha = conexao.execute("SELECT numero, produto FROM op WHERE numero = 24541").fetchone()
    print(linha, "->", linha[1])

    # sqlite3.Row: acesso por NOME da coluna (e também por posição)
    conexao.row_factory = sqlite3.Row
    linha = conexao.execute("SELECT numero, produto FROM op WHERE numero = 24541").fetchone()
    print(linha["produto"], "|", linha[0], "|", linha.keys())

    # Row vira dicionário com dict(...): ótimo para JSON, pandas, dataclasses
    ops = [dict(r) for r in conexao.execute("SELECT numero, status FROM op LIMIT 2")]
    print(ops)

print("Conexão fechada?", end=" ")
try:
    conexao.execute("SELECT 1")
except sqlite3.ProgrammingError as erro:
    print("sim ->", erro)
