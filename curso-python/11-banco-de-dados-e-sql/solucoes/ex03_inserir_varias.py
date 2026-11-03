"""
Exercício 11.03 — Inserir vários ensaios de uma vez (SOLUÇÃO)

Transação = "tudo ou nada". O "with conexao:" do sqlite3 faz exatamente isso:
  - terminou o bloco sem erro  -> commit (grava tudo);
  - deu exceção dentro do bloco -> rollback (desfaz tudo) e a exceção continua.
"""

import sqlite3


def inserir_ensaios(
    conexao: sqlite3.Connection, ensaios: list[tuple[int, int, str, float | None]]
) -> int:
    """Insere todos os ensaios numa transação e devolve a quantidade."""
    if not ensaios:
        return 0
    with conexao:
        conexao.executemany(
            "INSERT INTO ensaio (op, bobina, caracteristica, valor) VALUES (?, ?, ?, ?)",
            ensaios,
        )
    # Atenção: "with conexao" NÃO fecha a conexão; só controla a transação.
    return len(ensaios)
