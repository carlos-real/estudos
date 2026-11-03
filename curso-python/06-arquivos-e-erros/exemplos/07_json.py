"""Exemplo 07 — Regras de tolerância em JSON (seção 10).

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/07_json.py
"""

import json
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"

with open(DADOS / "regras_tolerancia.json", encoding="utf-8") as arquivo:
    regras = json.load(arquivo)

print("Linhas com regra:", sorted(regras))
for ensaio, regra in regras["A"].items():
    if "nominal" in regra:
        variacao = regra["nominal"] * regra["tolerancia_pct"] / 100
        minimo, maximo = regra["nominal"] - variacao, regra["nominal"] + variacao
    else:
        minimo, maximo = regra["min"], regra["max"]
    print(f"  Linha A, {ensaio:<10}: de {minimo:.2f} a {maximo:.2f}")

print("\nensure_ascii padrão:", json.dumps({"obs": "Liberação"}))
print("ensure_ascii=False :", json.dumps({"obs": "Liberação"}, ensure_ascii=False))

for texto in ["{'linha': 'A'}", '{"casas": 3\n "pasta": "laudos"}', '{"casas": 3}']:
    try:
        print("Lido:", json.loads(texto))
    except json.JSONDecodeError as erro:
        print(f"JSON quebrado na linha {erro.lineno}, coluna {erro.colno}: {erro.msg}")
