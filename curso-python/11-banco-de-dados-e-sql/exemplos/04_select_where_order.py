"""Exemplo 04 — SELECT: colunas, WHERE, ORDER BY, LIMIT, DISTINCT, LIKE, IS NULL, CASE.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/04_select_where_order.py
"""

from utilitarios import abrir_banco_exemplo, mostrar

banco = abrir_banco_exemplo()

mostrar(banco, "SELECT numero, linha, produto, quantidade_kg FROM op LIMIT 3")

mostrar(
    banco,
    """
    SELECT numero, produto, quantidade_kg / 1000 AS toneladas
    FROM op
    WHERE linha = 'A' AND quantidade_kg >= 4500
    ORDER BY quantidade_kg DESC
    """,
)

mostrar(banco, "SELECT DISTINCT status FROM op ORDER BY status")

mostrar(
    banco,
    """
    SELECT numero, emissao, status
    FROM op
    WHERE emissao BETWEEN '2026-10-21' AND '2026-10-22'
      AND status IN ('LIBERADA', 'CERTIFICADA')
    ORDER BY emissao, numero
    """,
)

mostrar(banco, "SELECT DISTINCT produto FROM op WHERE produto LIKE '%PE 35%'")

mostrar(banco, "SELECT op, bobina, caracteristica FROM ensaio WHERE valor IS NULL")

# Armadilha: "= NULL" nunca é verdadeiro. Esta consulta não acha nada!
mostrar(banco, "SELECT op, bobina FROM ensaio WHERE valor = NULL")

mostrar(
    banco,
    """
    SELECT numero, especificacao,
           CASE WHEN especificacao IS NULL THEN 'padrão da linha'
                ELSE 'especificação do cliente' END AS regra
    FROM op
    WHERE linha = 'A'
    """,
)
banco.close()
