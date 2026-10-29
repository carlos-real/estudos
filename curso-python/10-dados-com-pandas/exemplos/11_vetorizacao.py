"""Exemplo 11 — Vetorização x apply x laço for (com o seu script antigo de salários).

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/11_vetorizacao.py
"""

import time
from pathlib import Path

import pandas as pd

PASTA_MODULO = Path(__file__).resolve().parent.parent
ARQUIVO = PASTA_MODULO.parent.parent / "arquivos" / "salaries.csv"
if not ARQUIVO.exists():  # sem o arquivo grande, usa a amostra (os tempos ficam menores)
    ARQUIVO = PASTA_MODULO / "dados" / "salarios_amostra.csv"

df = pd.read_csv(ARQUIVO)
print(f"{len(df):,} linhas".replace(",", "."))

# Pergunta: quantos registros têm o cargo "Director"?

# 1) Laço for, como no script antigo: percorre linha a linha em Python puro.
inicio = time.perf_counter()
diretores = 0
for cargo in df["job_title"]:
    if cargo == "Director":
        diretores += 1
tempo_for = time.perf_counter() - inicio

# 2) apply: chama uma função Python para cada valor (ainda é um laço por dentro).
inicio = time.perf_counter()
diretores_apply = df["job_title"].apply(lambda cargo: cargo == "Director").sum()
tempo_apply = time.perf_counter() - inicio

# 3) Vetorizado: a comparação roda em código compilado, na coluna inteira.
inicio = time.perf_counter()
diretores_vet = (df["job_title"] == "Director").sum()
tempo_vet = time.perf_counter() - inicio

print("Resultados iguais?", diretores == diretores_apply == diretores_vet, "->", diretores)
print(f"for:         {tempo_for * 1000:8.2f} ms")
print(f"apply:       {tempo_apply * 1000:8.2f} ms")
print(f"vetorizado:  {tempo_vet * 1000:8.2f} ms")

# Outro exemplo: salário em milhares de dólares
inicio = time.perf_counter()
mil_apply = df["salary_in_usd"].apply(lambda valor: valor / 1000)
tempo_apply = time.perf_counter() - inicio
inicio = time.perf_counter()
mil_vet = df["salary_in_usd"] / 1000
tempo_vet = time.perf_counter() - inicio
print("Iguais?", mil_apply.equals(mil_vet))
print(f"apply: {tempo_apply * 1000:.2f} ms | vetorizado: {tempo_vet * 1000:.2f} ms")
