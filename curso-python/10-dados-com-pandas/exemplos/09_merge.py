"""Exemplo 09 — Juntar tabelas: merge (o PROCV do pandas) e concat.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/09_merge.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"
medicoes = pd.read_csv(
    DADOS / "medicoes.csv", sep=";", decimal=",", thousands=".", dtype={"op": str}
)
specs = pd.read_csv(DADOS / "especificacoes.csv", sep=";", decimal=",")
ops = pd.read_csv(
    DADOS / "ops_protheus.csv",
    sep=";",
    decimal=",",
    thousands=".",
    encoding="cp1252",
    dtype={"op": str},
)
print(specs[["produto", "espessura_nominal", "tolerancia_pct", "cof_max"]])

# 1) LEFT: todas as medições, com a especificação quando houver.
#    validate="many_to_one": muitas medições para UMA especificação por produto.
com_spec = medicoes.merge(specs, on="produto", how="left", validate="many_to_one")
print(com_spec.shape)
sem_spec = com_spec[com_spec["espessura_nominal"].isna()]
print("Produtos sem especificação:", sem_spec["produto"].unique().tolist())

# 2) Com a especificação ao lado, a conferência é uma conta vetorizada.
folga = com_spec["espessura_nominal"] * com_spec["tolerancia_pct"] / 100
com_spec["esp_min"] = com_spec["espessura_nominal"] - folga
com_spec["esp_max"] = com_spec["espessura_nominal"] + folga
fora = ~com_spec["espessura_um"].between(com_spec["esp_min"], com_spec["esp_max"])
fora = fora & com_spec["espessura_nominal"].notna()  # sem especificação não é "fora"
colunas = ["bobina", "produto", "espessura_um", "esp_min", "esp_max"]
print(com_spec.loc[fora, colunas].round(2))

# 3) INNER: só o que casa dos dois lados. Quem não casou SOME (cuidado!).
inner = medicoes.merge(ops[["op", "cliente"]], on="op", how="inner")
print("Medições:", len(medicoes), "| depois do inner com OPs:", len(inner))

# 4) indicator=True mostra de onde veio cada linha: both, left_only, right_only
checagem = medicoes.merge(ops[["op", "cliente"]], on="op", how="left", indicator=True)
print(checagem["_merge"].value_counts())
sem_cadastro = checagem.loc[checagem["_merge"] == "left_only", "op"].unique().tolist()
print("OP medida sem cadastro no ERP:", sem_cadastro)

# 5) Colunas com o mesmo nome nos dois lados ganham sufixos _x e _y
duplo = medicoes.merge(ops, on="op", how="inner")
print([c for c in duplo.columns if c.startswith("produto")])
duplo = medicoes.merge(ops, on="op", how="inner", suffixes=("_medido", "_erp"))
print([c for c in duplo.columns if c.startswith("produto")])

# 6) concat: empilhar tabelas com as MESMAS colunas (ex.: um CSV por mês)
julho = medicoes[medicoes["data"].str.endswith("/07/2026")]
agosto = medicoes[medicoes["data"].str.endswith("/08/2026")]
juntos = pd.concat([julho, agosto], ignore_index=True)
print(len(julho), "+", len(agosto), "=", len(juntos))
