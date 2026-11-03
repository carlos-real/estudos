"""
Exercício 11.02 — Inserir com parâmetros (SOLUÇÃO)

Regra de ouro: valores entram no SQL SEMPRE como parâmetros (?). Nunca monte o
comando com f-string: além de ser inseguro (SQL injection), o próprio sqlite3
cuida das aspas, dos números e do None.
"""

import sqlite3


def inserir_bobina(conexao: sqlite3.Connection, op: int, numero: int, peso_kg: float) -> int:
    """Insere a bobina, grava e devolve o id gerado."""
    cursor = conexao.execute(
        "INSERT INTO bobina (op, numero, peso_kg) VALUES (?, ?, ?)",
        (op, numero, peso_kg),
    )
    conexao.commit()  # sem commit, outra conexão (outro programa) não vê a bobina
    return cursor.lastrowid  # o id que o SQLite acabou de gerar


def contar_bobinas(conexao: sqlite3.Connection, op: int) -> int:
    """Quantidade de bobinas da OP."""
    # COUNT(*) sempre devolve exatamente uma linha (com 0 se não houver nada).
    (quantidade,) = conexao.execute("SELECT COUNT(*) FROM bobina WHERE op = ?", (op,)).fetchone()
    return quantidade
