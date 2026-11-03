"""Exemplo 10 — Tabela dinâmica: pivot_table, crosstab e melt.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/10_pivot_table.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"
df = pd.read_csv(
    DADOS / "medicoes.csv", sep=";", decimal=",", thousands=".", dtype={"op": str}
)
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
df["mes"] = df["data"].dt.strftime("%Y-%m")

# 1) Peso produzido: linhas nas linhas, meses nas colunas (igual à tabela dinâmica do Excel)
tabela = pd.pivot_table(
    df,
    index="linha",
    columns="mes",
    values="peso_kg",
    aggfunc="sum",
    fill_value=0,
    margins=True,  # linha e coluna de total
    margins_name="Total",
)
print(tabela.round(0))

# 2) Média de COF por linha e mês, só para conferir tendência
print(df.pivot_table(index="linha", columns="mes", values="cof", aggfunc="mean").round(3))

# 3) crosstab: contar combinações (quantas bobinas por linha e mês)
print(pd.crosstab(df["linha"], df["mes"]))

# 4) melt: o caminho inverso. Planilha "larga" (um mês por coluna) -> tabela "longa".
larga = pd.DataFrame(
    {"linha": ["A", "B"], "jul": [33.2, 18.5], "ago": [22.1, 12.0], "set": [29.7, 15.3]}
)
longa = larga.melt(id_vars="linha", var_name="mes", value_name="toneladas")
print(larga)
print(longa)
