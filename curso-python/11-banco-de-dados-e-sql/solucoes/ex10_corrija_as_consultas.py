"""
Exercício 11.10 — Corrija as consultas (SOLUÇÃO)

Os três defeitos são clássicos (e aparecem em entrevista de emprego):

(1) "valor = NULL" nunca é verdadeiro. NULL significa "desconhecido", e
    desconhecido = desconhecido também é desconhecido. Use IS NULL / IS NOT NULL.

(2) No LEFT JOIN, a OP sem ensaio vira UMA linha com as colunas de ensaio NULL.
    COUNT(*) conta essa linha (dá 1). COUNT(e.id) conta só valores não nulos (dá 0).

(3) O WHERE roda DEPOIS do LEFT JOIN. Nas linhas sem par, o.linha é NULL, e
    "NULL = 'B'" não é verdadeiro: o WHERE joga fora justamente os clientes que o
    LEFT JOIN tinha guardado. A condição sobre a tabela da direita vai no ON.
"""

import sqlite3


def ensaios_sem_valor(conexao: sqlite3.Connection) -> list[tuple[int, int, str]]:
    """Ensaios ainda sem valor."""
    sql = """
        SELECT op, bobina, caracteristica
        FROM ensaio
        WHERE valor IS NULL
        ORDER BY op, bobina, caracteristica
    """
    return conexao.execute(sql).fetchall()


def ensaios_por_op(conexao: sqlite3.Connection) -> list[tuple[int, int]]:
    """Quantidade de ensaios de cada OP (0 se nenhum)."""
    sql = """
        SELECT o.numero, COUNT(e.id)
        FROM op AS o
        LEFT JOIN ensaio AS e ON e.op = o.numero
        GROUP BY o.numero
        ORDER BY o.numero
    """
    return conexao.execute(sql).fetchall()


def clientes_e_ops_da_linha(
    conexao: sqlite3.Connection, linha: str
) -> list[tuple[str, int | None]]:
    """Todos os clientes com as OPs da linha (ou None)."""
    sql = """
        SELECT c.nome, o.numero
        FROM cliente AS c
        LEFT JOIN op AS o ON o.cliente_id = c.id AND o.linha = ?
        ORDER BY c.nome, o.numero
    """
    return conexao.execute(sql, (linha,)).fetchall()
