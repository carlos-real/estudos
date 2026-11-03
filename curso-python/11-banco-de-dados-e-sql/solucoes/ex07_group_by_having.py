"""
Exercício 11.07 — GROUP BY e HAVING (SOLUÇÃO)

Ordem em que o banco "pensa" (não é a ordem em que escrevemos!):
    FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
Por isso o WHERE não enxerga COUNT(*) (os grupos ainda não existem) e o HAVING sim.
"""

import sqlite3


def fora_por_caracteristica(conexao: sqlite3.Connection) -> list[tuple[str, int]]:
    """Quantidade de ensaios FORA por característica."""
    # Filtrar no WHERE já deixa só os FORA; quem não tem nenhum nem vira grupo.
    sql = """
        SELECT caracteristica, COUNT(*) AS quantidade
        FROM ensaio
        WHERE resultado = 'FORA'
        GROUP BY caracteristica
        ORDER BY quantidade DESC, caracteristica
    """
    return conexao.execute(sql).fetchall()


def ops_com_varias_cargas(
    conexao: sqlite3.Connection, minimo: int
) -> list[tuple[int, int, float]]:
    """OPs com pelo menos `minimo` cargas expedidas."""
    sql = """
        SELECT op, COUNT(*) AS cargas, SUM(peso_kg) AS peso_total
        FROM expedicao
        GROUP BY op
        HAVING COUNT(*) >= ?
        ORDER BY op
    """
    return conexao.execute(sql, (minimo,)).fetchall()
