"""Exemplo 15 — Laboratório guiado: o mercado de dados em 133 mil salários.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/15_laboratorio_salarios.py

Usa ../arquivos/salaries.csv (a partir da pasta curso-python). Se o arquivo não
existir, usa a amostra pequena de dados/salarios_amostra.csv (números diferentes).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pandas as pd

PASTA_MODULO = Path(__file__).resolve().parent.parent
ARQUIVO = PASTA_MODULO / ".." / ".." / "arquivos" / "salaries.csv"
if not ARQUIVO.exists():
    print("(arquivo grande não encontrado: usando a amostra de 600 linhas)")
    ARQUIVO = PASTA_MODULO / "dados" / "salarios_amostra.csv"
SAIDA = PASTA_MODULO / "saida"
SAIDA.mkdir(exist_ok=True)

NIVEIS = {"EN": "Júnior", "MI": "Pleno", "SE": "Sênior", "EX": "Executivo"}
REGIME = {0: "Presencial", 50: "Híbrido", 100: "Remoto"}

df = pd.read_csv(ARQUIVO)

print("=== 0. Conhecendo a base ===")
print(df.shape)
print("Anos:", df["work_year"].value_counts().sort_index().to_dict())
print("work_year vazio:", df["work_year"].isna().sum())
print("Linhas idênticas a outra:", df.duplicated().sum())

# work_year veio como float (2024.0) porque tem vazios. "Int64" (com I maiúsculo)
# é o inteiro do pandas que aceita ausentes (<NA>).
df["work_year"] = df["work_year"].astype("Int64")

# Preparação: só tempo integral (FT) e nomes em português
df = df[df["employment_type"] == "FT"].copy()
df["nivel"] = pd.Categorical(
    df["experience_level"].map(NIVEIS), categories=list(NIVEIS.values()), ordered=True
)
df["regime"] = df["remote_ratio"].map(REGIME)
df["salario_mil_usd"] = df["salary_in_usd"] / 1000

print("\n=== 1. Quanto ganha cada nível? (mil USD/ano) ===")
por_nivel = df.groupby("nivel", observed=True)["salario_mil_usd"].agg(
    ["count", "median", "mean"]
)
print(por_nivel.round(1))

print("\n=== 2. Quais cargos aparecem mais? ===")
print("Cargos diferentes:", df["job_title"].nunique())
print(df["job_title"].value_counts().head(8))

print("\n=== 3. Cargo x nível (mediana, mil USD) ===")
cargos = ["Data Analyst", "Data Engineer", "Data Scientist", "Analytics Engineer"]
tabela = df[df["job_title"].isin(cargos)].pivot_table(
    index="job_title", columns="nivel", values="salario_mil_usd", aggfunc="median",
    observed=True,
)  # fmt: skip
print(tabela.round(1))

print("\n=== 4. Trabalho remoto paga menos? ===")
print(df.groupby("regime")["salario_mil_usd"].agg(["count", "median"]).round(1))
eua_2025 = df[(df["company_location"] == "US") & (df["work_year"] == 2025)]
print("Só empresas dos EUA em 2025:")
print(
    eua_2025.pivot_table(
        index="nivel", columns="regime", values="salario_mil_usd", aggfunc="median",
        observed=True,
    ).round(1)
)  # fmt: skip
print("Registros híbridos nessa fatia:", (eua_2025["regime"] == "Híbrido").sum())

print("\n=== 5. E quem mora no Brasil? ===")
brasil = df[df["employee_residence"] == "BR"]
print("Registros:", len(brasil))
print(brasil.groupby("nivel", observed=True)["salario_mil_usd"].agg(["count", "median"]).round(1))

print("\n=== 6. Evolução por ano (mediana, mil USD) ===")
print(df.groupby("work_year")["salario_mil_usd"].median().round(1))

# Gráfico para o portfólio
ax = por_nivel["median"].plot.bar(color="#1F4E78", rot=0)
ax.set_title("Salário mediano por nível (tempo integral)")
ax.set_xlabel("Nível")
ax.set_ylabel("Mil USD por ano")
ax.figure.tight_layout()
ax.figure.savefig(SAIDA / "salario_por_nivel.png", dpi=120)
print("\nGráfico salvo em saida/salario_por_nivel.png")
