"""Exemplo 04 — Inspecionar uma tabela e selecionar linhas e colunas.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/04_inspecionar_e_selecionar.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"
df = pd.read_csv(
    DADOS / "medicoes.csv", sep=";", decimal=",", thousands=".", dtype={"op": str}
)

# --- Inspecionar: os 5 comandos para qualquer base nova ---
print(df.shape)
df.info()
print(df[["espessura_um", "cof", "peso_kg"]].describe().round(2))
print(df["linha"].value_counts())
print("Produtos:", sorted(df["produto"].unique()))
print("Quantas OPs diferentes:", df["op"].nunique())

# --- Selecionar colunas ---
print(df["cof"].head(3))  # uma coluna -> Series
print(df[["op", "cof"]].head(3))  # lista de colunas -> DataFrame

# --- loc (por RÓTULO) e iloc (por POSIÇÃO) ---
print(df.loc[0, "bobina"])  # linha de rótulo 0, coluna "bobina"
print(df.loc[0:2, ["bobina", "cof"]])  # loc inclui o fim (0, 1 e 2)
print(df.iloc[0:2, 0:3])  # iloc exclui o fim, como fatias de lista

# --- Filtros booleanos ---
mascara = df["cof"] > 0.35
print(mascara.head(3))
print("Bobinas com COF > 0,35:", mascara.sum())
print(df[mascara][["bobina", "linha", "cof", "observacao"]])

# Duas condições: use & (e), | (ou), ~ (não) e PARÊNTESES em cada condição.
linha_a_grossa = df[(df["linha"] == "A") & (df["espessura_um"] > 48)]
print(linha_a_grossa[["bobina", "produto", "espessura_um"]])

# isin: "está nesta lista?"; between: "está na faixa?" (inclui as pontas)
print(len(df[df["linha"].isin(["C", "D"])]), "bobinas nas linhas C e D")
dentro = df["espessura_um"].between(57.66, 66.34)  # LAM-62: 62 µm ± 7%
print(df[(df["produto"] == "LAM-62") & ~dentro][["bobina", "espessura_um"]])

# Filtro + seleção de colunas numa tacada só, com loc:
print(df.loc[df["observacao"].notna(), ["bobina", "cof", "observacao"]])
