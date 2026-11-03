"""Exemplo 02 — Ler CSV no padrão brasileiro (Excel em português).

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/02_ler_csv_brasileiro.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"

# 1) Leitura ingênua: o pandas espera vírgula como separador.
ingenuo = pd.read_csv(DADOS / "medicoes.csv")
print("Leitura ingênua -> formato:", ingenuo.shape)

# 2) Leitura correta para CSV salvo pelo Excel brasileiro.
df = pd.read_csv(
    DADOS / "medicoes.csv",
    sep=";",  # separador de colunas
    decimal=",",  # vírgula decimal: 47,7 -> 47.7
    thousands=".",  # ponto de milhar: 1.558,5 -> 1558.5
    encoding="utf-8-sig",  # UTF-8 com BOM (o "CSV UTF-8" do Excel)
    dtype={"op": str},  # OP é código, não número: preserva o zero à esquerda
)
print("Leitura correta -> formato:", df.shape)
print(df[["op", "bobina", "espessura_um", "cof", "peso_kg"]].head())
print(df.dtypes)

# 3) O que acontece se esquecer o dtype da OP?
sem_dtype = pd.read_csv(DADOS / "medicoes.csv", sep=";", decimal=",", thousands=".")
print("OP sem dtype:", sem_dtype.loc[0, "op"], "| OP com dtype:", df.loc[0, "op"])

# 4) Arquivo exportado do ERP em cp1252 (padrão antigo do Windows).
try:
    pd.read_csv(DADOS / "ops_protheus.csv", sep=";")
except UnicodeDecodeError as erro:
    print("Erro de encoding:", erro)

ops = pd.read_csv(
    DADOS / "ops_protheus.csv",
    sep=";",
    decimal=",",
    thousands=".",
    encoding="cp1252",
    dtype={"op": str},
)
print(ops[["op", "cliente", "quantidade_kg"]].head(4))

# 5) Espiar só o começo de um arquivo grande: nrows e usecols.
espiada = pd.read_csv(
    DADOS / "medicoes.csv",
    sep=";",
    decimal=",",
    usecols=["op", "linha", "espessura_um"],
    nrows=3,
    dtype={"op": str},
)
print(espiada)
