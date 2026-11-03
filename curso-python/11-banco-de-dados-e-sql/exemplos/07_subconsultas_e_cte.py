"""Exemplo 07 — Subconsultas (IN, escalar, EXISTS) e CTE (WITH).

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/07_subconsultas_e_cte.py
"""

from utilitarios import abrir_banco_exemplo, mostrar

banco = abrir_banco_exemplo()

# Subconsulta escalar: devolve UM valor (a média) para comparar
mostrar(
    banco,
    """
    SELECT numero, quantidade_kg
    FROM op
    WHERE quantidade_kg > (SELECT AVG(quantidade_kg) FROM op)
    ORDER BY quantidade_kg DESC
    """,
)

# IN (subconsulta): OPs com pelo menos um ensaio FORA
mostrar(
    banco,
    """
    SELECT numero, status
    FROM op
    WHERE numero IN (SELECT op FROM ensaio WHERE resultado = 'FORA')
    """,
)

# NOT EXISTS: clientes sem nenhuma OP
mostrar(
    banco,
    """
    SELECT nome
    FROM cliente AS c
    WHERE NOT EXISTS (SELECT 1 FROM op AS o WHERE o.cliente_id = c.id)
    """,
)

# CTE (WITH): dá nome a um passo intermediário. Lê-se de cima para baixo.
mostrar(
    banco,
    """
    WITH situacao AS (
        SELECT op,
               SUM(resultado = 'FORA') AS fora,
               SUM(valor IS NULL) AS pendentes
        FROM ensaio
        GROUP BY op
    )
    SELECT o.numero, o.status, s.fora, s.pendentes
    FROM op AS o
    JOIN situacao AS s ON s.op = o.numero
    WHERE s.fora > 0 OR s.pendentes > 0
    ORDER BY o.numero
    """,
)
banco.close()
