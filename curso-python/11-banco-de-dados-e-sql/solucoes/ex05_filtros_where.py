"""
Exercício 11.05 — Filtros com WHERE (SOLUÇÃO)
"""

import sqlite3


def ops_da_linha_no_periodo(
    conexao: sqlite3.Connection, linha: str, inicio: str, fim: str
) -> list[int]:
    """Números das OPs da linha emitidas no período (inclusive)."""
    # Datas em texto ISO ('AAAA-MM-DD') comparam certo como texto: por isso o
    # banco guarda assim. BETWEEN inclui as duas pontas.
    sql = """
        SELECT numero
        FROM op
        WHERE linha = ? AND emissao BETWEEN ? AND ?
        ORDER BY emissao, numero
    """
    # Cada linha vem como tupla de 1 elemento: (24518,). O desempacotamento
    # "for (numero,) in ..." tira o valor de dentro.
    return [numero for (numero,) in conexao.execute(sql, (linha, inicio, fim))]


def ensaios_pendentes(conexao: sqlite3.Connection) -> list[tuple[int, int, str]]:
    """Ensaios ainda sem valor."""
    # NULL não é igual a nada, nem a outro NULL: "valor = NULL" nunca é verdade.
    sql = """
        SELECT op, bobina, caracteristica
        FROM ensaio
        WHERE valor IS NULL
        ORDER BY op, bobina, caracteristica
    """
    return conexao.execute(sql).fetchall()


def buscar_produtos(conexao: sqlite3.Connection, trecho: str) -> list[str]:
    """Produtos (sem repetição) que contêm o trecho."""
    # O % (qualquer coisa) fica no SQL, concatenado com || ao parâmetro. Assim o
    # trecho continua sendo um parâmetro, sem f-string. No SQLite, LIKE já ignora
    # maiúsculas/minúsculas (para letras sem acento).
    sql = """
        SELECT DISTINCT produto
        FROM op
        WHERE produto LIKE '%' || ? || '%'
        ORDER BY produto
    """
    return [produto for (produto,) in conexao.execute(sql, (trecho,))]
    # Alternativa: passar o padrão pronto: conexao.execute("... LIKE ?", (f"%{trecho}%",))
