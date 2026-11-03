"""Exemplo 06 — JOINs: INNER, LEFT, "quem não tem" e três tabelas.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/06_joins.py
"""

from utilitarios import abrir_banco_exemplo, mostrar

banco = abrir_banco_exemplo()

# INNER JOIN: só as linhas que casam dos dois lados
mostrar(
    banco,
    """
    SELECT o.numero, c.nome AS cliente, o.produto
    FROM op AS o
    JOIN cliente AS c ON c.id = o.cliente_id
    WHERE o.linha = 'D'
    ORDER BY o.numero
    """,
)

# LEFT JOIN: todos da esquerda, mesmo sem par (as colunas da direita vêm NULL)
mostrar(
    banco,
    """
    SELECT c.nome, o.numero
    FROM cliente AS c
    LEFT JOIN op AS o ON o.cliente_id = c.id
    WHERE c.uf = 'MG'
    ORDER BY c.nome, o.numero
    """,
)

# "Quem NÃO tem": LEFT JOIN + IS NULL do lado direito
mostrar(
    banco,
    """
    SELECT o.numero, o.status
    FROM op AS o
    LEFT JOIN ensaio AS e ON e.op = o.numero
    WHERE e.id IS NULL
    """,
)

# Três tabelas + agregação: peso expedido por cliente
mostrar(
    banco,
    """
    SELECT c.nome AS cliente, COUNT(x.id) AS cargas, SUM(x.peso_kg) AS peso_kg
    FROM expedicao AS x
    JOIN op AS o ON o.numero = x.op
    JOIN cliente AS c ON c.id = o.cliente_id
    GROUP BY c.nome
    ORDER BY peso_kg DESC
    """,
)

# Erro comum: condição da tabela da direita no WHERE "desfaz" o LEFT JOIN
mostrar(
    banco,
    """
    SELECT c.nome, o.numero
    FROM cliente AS c
    LEFT JOIN op AS o ON o.cliente_id = c.id
    WHERE c.uf = 'MG' AND o.linha = 'B'
    """,
)
mostrar(
    banco,
    """
    SELECT c.nome, o.numero
    FROM cliente AS c
    LEFT JOIN op AS o ON o.cliente_id = c.id AND o.linha = 'B'
    WHERE c.uf = 'MG'
    """,
)
banco.close()
