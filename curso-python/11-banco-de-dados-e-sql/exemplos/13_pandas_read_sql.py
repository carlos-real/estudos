"""Exemplo 13 — pandas e SQL juntos: read_sql (com parâmetros) e to_sql.

Rode (na pasta curso-python):
    python 11-banco-de-dados-e-sql/exemplos/13_pandas_read_sql.py
"""

import pandas as pd
from utilitarios import abrir_banco_exemplo

banco = abrir_banco_exemplo()

# SQL faz o trabalho pesado (filtrar, juntar, agregar); pandas recebe a tabela pronta
consulta = """
    SELECT o.linha, e.caracteristica, e.valor
    FROM ensaio AS e
    JOIN op AS o ON o.numero = e.op
    WHERE e.caracteristica = ? AND e.valor IS NOT NULL
"""
df = pd.read_sql(consulta, banco, params=("espessura",))
print(df.head(3))
print(df.groupby("linha")["valor"].agg(["count", "mean"]).round(2))

# E o caminho inverso: um DataFrame vira tabela no banco
metas = pd.DataFrame({"linha": ["A", "B", "C", "D"], "meta_t_mes": [60, 40, 30, 45]})
metas.to_sql("meta", banco, index=False, if_exists="replace")
print(banco.execute("SELECT * FROM meta WHERE meta_t_mes >= 45").fetchall())
banco.close()
