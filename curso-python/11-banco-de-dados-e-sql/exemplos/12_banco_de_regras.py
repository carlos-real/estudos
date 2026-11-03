"""Exemplo 12 — O banco de regras do projeto final: especificação e tolerâncias.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/12_banco_de_regras.py
"""

import sqlite3

from utilitarios import abrir_banco_exemplo, mostrar

regras = abrir_banco_exemplo("regras.sql")

# 1) O padrão de cada linha
mostrar(regras, "SELECT titulo, linha FROM especificacao WHERE linha IS NOT NULL")

# 2) Tolerâncias do padrão da linha A
mostrar(
    regras,
    """
    SELECT t.caracteristica, t.tipo, t.minimo, t.maximo, t.percentual
    FROM tolerancia AS t
    JOIN especificacao AS e ON e.titulo = t.titulo
    WHERE e.linha = ?
    ORDER BY t.caracteristica
    """,
    ("A",),
)

# 3) Tolerâncias EFETIVAS de uma OP da linha A com a especificação ESP-0533:
#    as da especificação + as do padrão que a especificação NÃO redefine.
EFETIVAS = """
    SELECT caracteristica, tipo, minimo, maximo, percentual, titulo AS origem
    FROM tolerancia
    WHERE titulo = :titulo
    UNION ALL
    SELECT t.caracteristica, t.tipo, t.minimo, t.maximo, t.percentual, t.titulo
    FROM tolerancia AS t
    JOIN especificacao AS e ON e.titulo = t.titulo
    WHERE e.linha = :linha
      AND t.caracteristica NOT IN (
          SELECT caracteristica FROM tolerancia WHERE titulo = :titulo
      )
    ORDER BY caracteristica
"""
mostrar(regras, EFETIVAS, {"linha": "A", "titulo": "ESP-0533"})

# 4) Tolerância nominal vira faixa com o valor nominal da planilha (60 µm ± 5%)
nominal, percentual = 60.0, 5.0
folga = nominal * percentual / 100
print(f"Espessura: {nominal} ± {percentual}% -> {nominal - folga:g} a {nominal + folga:g} µm")

# 5) As restrições protegem as regras
try:
    regras.execute("INSERT INTO especificacao (titulo, linha) VALUES ('OUTRO-PADRAO-A', 'A')")
except sqlite3.IntegrityError as erro:
    print("Segundo padrão para a linha A ->", erro)
try:
    regras.execute(
        "INSERT INTO tolerancia (titulo, caracteristica, tipo) "
        "VALUES ('ESP-0412', 'cor', 'livre')"
    )
except sqlite3.IntegrityError as erro:
    print("Tipo inválido ->", erro)
regras.close()
