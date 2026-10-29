"""Exemplo 08 — Agrupar e resumir: groupby, agg, size, transform.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/08_groupby_agg.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"
df = pd.read_csv(
    DADOS / "medicoes.csv", sep=";", decimal=",", thousands=".", dtype={"op": str}
)

# 1) Uma estatística de uma coluna por grupo -> Series
print(df.groupby("linha")["peso_kg"].sum())

# 2) Várias estatísticas: agg com "agregação nomeada" (nome_novo=(coluna, função))
resumo = df.groupby("linha").agg(
    bobinas=("bobina", "count"),
    ops=("op", "nunique"),
    peso_total_kg=("peso_kg", "sum"),
    cof_medio=("cof", "mean"),
    cof_max=("cof", "max"),
)
print(resumo.round(3))

# 3) Agrupar por duas colunas e devolver colunas normais (as_index=False)
por_produto = df.groupby(["linha", "produto"], as_index=False).agg(
    media_um=("espessura_um", "mean"),
    desvio_um=("espessura_um", "std"),
)
print(por_produto.round(2))

# 4) Percentual de bobinas com COF acima de 0,30 por linha.
#    Truque: a média de uma coluna True/False é a proporção de True.
df["cof_alto"] = df["cof"] > 0.30
print((df.groupby("linha")["cof_alto"].mean() * 100).round(1))

# 5) size() conta linhas; count() conta valores NÃO ausentes de cada coluna
print(df.groupby("linha").size())
print(df.groupby("linha")["observacao"].count())

# 6) transform devolve um valor POR LINHA (do tamanho da tabela original).
#    Útil para comparar cada bobina com a média da própria OP.
df["media_da_op"] = df.groupby("op")["espessura_um"].transform("mean")
df["dif_da_op"] = (df["espessura_um"] - df["media_da_op"]).round(2)
print(df[["bobina", "espessura_um", "media_da_op", "dif_da_op"]].head(4).round(2))

# 7) Ordenar o resumo: as linhas com mais peso primeiro
print(resumo.sort_values("peso_total_kg", ascending=False).head(2)[["peso_total_kg"]])
