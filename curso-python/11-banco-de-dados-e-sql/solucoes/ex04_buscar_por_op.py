"""
Exercício 11.04 — Buscar os ensaios de uma OP (SOLUÇÃO)

Sem ORDER BY, o banco devolve as linhas "na ordem que achar melhor". Hoje pode
coincidir com a ordem de inserção; amanhã, com um índice novo, muda. Se a ordem
importa (e num certificado importa), peça explicitamente.
"""

import sqlite3


def ensaios_da_op(conexao: sqlite3.Connection, op: int) -> list[tuple[int, str, float | None]]:
    """(bobina, caracteristica, valor) da OP, ordenados."""
    sql = """
        SELECT bobina, caracteristica, valor
        FROM ensaio
        WHERE op = ?
        ORDER BY bobina, caracteristica
    """
    return conexao.execute(sql, (op,)).fetchall()


def existe_op(conexao: sqlite3.Connection, numero: int) -> bool:
    """A OP está cadastrada?"""
    # "SELECT 1" basta: não precisamos dos dados, só saber se há linha.
    linha = conexao.execute("SELECT 1 FROM op WHERE numero = ?", (numero,)).fetchone()
    return linha is not None
