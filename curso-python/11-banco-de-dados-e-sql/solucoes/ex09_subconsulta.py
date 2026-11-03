"""
Exercício 11.09 — Subconsultas (SOLUÇÃO)

Leia uma subconsulta de dentro para fora: primeiro a pergunta de dentro (a
média, a lista de OPs com FORA), depois a de fora usa a resposta.
"""

import sqlite3


def ops_acima_da_media(conexao: sqlite3.Connection) -> list[tuple[int, float]]:
    """OPs com quantidade acima da média."""
    # Subconsulta ESCALAR: devolve um valor só, usado como um número qualquer.
    sql = """
        SELECT numero, quantidade_kg
        FROM op
        WHERE quantidade_kg > (SELECT AVG(quantidade_kg) FROM op)
        ORDER BY quantidade_kg DESC
    """
    return conexao.execute(sql).fetchall()


def ops_com_reprovacao(conexao: sqlite3.Connection) -> list[int]:
    """OPs com algum ensaio FORA."""
    # Subconsulta com IN: devolve uma LISTA de valores. Repetições não importam
    # (a OP 24533 tem dois FORA, mas aparece uma vez só, porque vem da tabela op).
    sql = """
        SELECT numero
        FROM op
        WHERE numero IN (SELECT op FROM ensaio WHERE resultado = 'FORA')
        ORDER BY numero
    """
    return [numero for (numero,) in conexao.execute(sql)]


def clientes_sem_op(conexao: sqlite3.Connection) -> list[str]:
    """Clientes sem nenhuma OP."""
    # Subconsulta CORRELACIONADA: o c.id de fora entra na de dentro.
    # NOT EXISTS é verdadeiro quando a de dentro não acha nenhuma linha.
    sql = """
        SELECT nome
        FROM cliente AS c
        WHERE NOT EXISTS (SELECT 1 FROM op AS o WHERE o.cliente_id = c.id)
        ORDER BY nome
    """
    return [nome for (nome,) in conexao.execute(sql)]
    # Cuidado com a alternativa "id NOT IN (SELECT cliente_id FROM op)": se a
    # subconsulta tiver algum NULL, o NOT IN não devolve NADA. NOT EXISTS é seguro.
