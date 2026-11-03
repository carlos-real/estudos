"""Exemplo 05 — Agregação: COUNT, SUM, AVG, MIN, MAX, GROUP BY e HAVING.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/05_agregacao_group_by.py
"""

from utilitarios import abrir_banco_exemplo, mostrar

banco = abrir_banco_exemplo()

mostrar(
    banco,
    """
    SELECT COUNT(*) AS ops, SUM(quantidade_kg) AS total_kg,
           ROUND(AVG(quantidade_kg), 1) AS media_kg,
           MIN(emissao) AS primeira, MAX(emissao) AS ultima
    FROM op
    """,
)

# COUNT(*) conta linhas; COUNT(coluna) conta valores NÃO nulos
mostrar(
    banco,
    """
    SELECT COUNT(*) AS linhas, COUNT(valor) AS medidos
    FROM ensaio
    WHERE caracteristica = 'cof'
    """,
)

mostrar(
    banco,
    """
    SELECT linha, COUNT(*) AS ops, SUM(quantidade_kg) AS total_kg
    FROM op
    GROUP BY linha
    ORDER BY total_kg DESC
    """,
)

mostrar(
    banco,
    """
    SELECT caracteristica, COUNT(*) AS ensaios,
           SUM(CASE WHEN resultado = 'FORA' THEN 1 ELSE 0 END) AS fora
    FROM ensaio
    GROUP BY caracteristica
    """,
)

# WHERE filtra LINHAS antes de agrupar; HAVING filtra GRUPOS depois.
mostrar(
    banco,
    """
    SELECT op, COUNT(*) AS cargas, SUM(peso_kg) AS peso_total
    FROM expedicao
    WHERE data >= '2026-10-26'
    GROUP BY op
    HAVING COUNT(*) >= 2
    ORDER BY op
    """,
)
banco.close()
