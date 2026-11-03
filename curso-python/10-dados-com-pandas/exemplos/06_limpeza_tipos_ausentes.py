"""Exemplo 06 — Limpeza: tipos, texto, valores ausentes e duplicatas.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/06_limpeza_tipos_ausentes.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"

# Lemos TUDO como texto (dtype=str) para ver os dados como foram digitados.
bruto = pd.read_csv(DADOS / "medicoes_sujas.csv", sep=";", dtype=str)
print(bruto)

# --- 1. Diagnóstico ---
print(bruto["linha"].unique().tolist())
print(bruto.isna().sum())

df = bruto.copy()

# --- 2. Texto: tirar espaços e padronizar maiúsculas ---
df["linha"] = df["linha"].str.strip().str.upper()
df["operador"] = df["operador"].str.strip().str.title()
print(df["linha"].unique().tolist(), df["operador"].unique().tolist())

# --- 3. Números brasileiros guardados como texto ---
# "1.120,5" -> tira o ponto de milhar -> troca a vírgula por ponto -> 1120.5
df["peso_kg"] = pd.to_numeric(
    df["peso_kg"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
)
# errors="coerce": o que não for número (como "n/d") vira NaN em vez de dar erro.
df["espessura_um"] = pd.to_numeric(
    df["espessura_um"].str.strip().str.replace(",", ".", regex=False), errors="coerce"
)
print(df[["bobina", "espessura_um", "peso_kg"]])
print(df.dtypes)

# --- 4. Duplicatas ---
print("Linhas idênticas repetidas:", df.duplicated().sum())
print("Bobinas repetidas:", df.duplicated(subset=["bobina"]).sum())
df = df.drop_duplicates(subset=["bobina"], keep="first")

# --- 5. Ausentes: decidir caso a caso ---
sem_espessura = df[df["espessura_um"].isna()]
print("Sem espessura:", sem_espessura["bobina"].tolist())
df = df.dropna(subset=["espessura_um"])  # sem medição, não dá para avaliar
df["peso_kg"] = df["peso_kg"].fillna(0)  # peso ausente: anotar 0 e avisar alguém
df = df.reset_index(drop=True)
print(df[["data", "linha", "bobina", "espessura_um", "peso_kg", "operador"]])
