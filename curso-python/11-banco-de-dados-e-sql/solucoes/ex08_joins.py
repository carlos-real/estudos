"""
Exercício 11.08 — JOINs (SOLUÇÃO)

INNER JOIN: só o que casa dos dois lados.
LEFT JOIN: tudo da tabela da esquerda; sem par, as colunas da direita vêm NULL.
"""

import sqlite3


def relatorio_ops(conexao: sqlite3.Connection, linha: str) -> list[dict]:
    """OPs da linha com o nome do cliente."""
    sql = """
        SELECT o.numero, c.nome AS cliente, o.produto
        FROM op AS o
        JOIN cliente AS c ON c.id = o.cliente_id
        WHERE o.linha = ?
        ORDER BY o.numero
    """
    cursor = conexao.execute(sql, (linha,))
    # cursor.description traz os nomes das colunas (já com os apelidos do AS).
    nomes = [coluna[0] for coluna in cursor.description]
    return [dict(zip(nomes, linha_banco, strict=True)) for linha_banco in cursor]
    # Alternativa: conexao.row_factory = sqlite3.Row e dict(linha). Mas mudar a
    # row_factory muda a conexão de quem chamou: aqui preferimos não mexer.


def ops_sem_ensaio(conexao: sqlite3.Connection) -> list[int]:
    """OPs sem nenhum ensaio."""
    # O "anti-join": LEFT JOIN e depois ficar só com quem NÃO achou par.
    sql = """
        SELECT o.numero
        FROM op AS o
        LEFT JOIN ensaio AS e ON e.op = o.numero
        WHERE e.id IS NULL
        ORDER BY o.numero
    """
    return [numero for (numero,) in conexao.execute(sql)]
    # Alternativa: WHERE NOT EXISTS (SELECT 1 FROM ensaio WHERE ensaio.op = op.numero)


def peso_por_cliente(conexao: sqlite3.Connection) -> list[tuple[str, float]]:
    """Peso expedido por cliente (todos os clientes)."""
    # Dois LEFT JOIN seguidos mantêm o cliente mesmo sem OP, e a OP mesmo sem
    # carga. SUM de nada é NULL; COALESCE troca por 0.0.
    sql = """
        SELECT c.nome, COALESCE(SUM(x.peso_kg), 0.0) AS peso
        FROM cliente AS c
        LEFT JOIN op AS o ON o.cliente_id = c.id
        LEFT JOIN expedicao AS x ON x.op = o.numero
        GROUP BY c.id, c.nome
        ORDER BY peso DESC, c.nome
    """
    return conexao.execute(sql).fetchall()
