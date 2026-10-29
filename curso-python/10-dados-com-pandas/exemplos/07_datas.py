"""Exemplo 07 — Datas: converter dd/mm/aaaa, extrair partes, filtrar e agrupar por mês.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/07_datas.py
"""

from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parent.parent / "dados"
df = pd.read_csv(
    DADOS / "medicoes.csv", sep=";", decimal=",", thousands=".", dtype={"op": str}
)
print("Antes:", df["data"].dtype, "| exemplo:", df.loc[0, "data"])

# 1) Texto -> data. Diga o formato: dia/mês/ano.
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
print("Depois:", df["data"].dtype, "| exemplo:", df.loc[0, "data"])

# 2) O perigo de NÃO dizer o formato: "03/07/2026" vira 7 de março!
ambigua = pd.to_datetime(pd.Series(["03/07/2026"]))
print("Sem formato:", ambigua[0].date())
print("dayfirst=True:", pd.to_datetime(pd.Series(["03/07/2026"]), dayfirst=True)[0].date())

# 3) Extrair partes com .dt
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month
df["mes_ano"] = df["data"].dt.strftime("%m/%Y")
df["dia_semana"] = df["data"].dt.dayofweek  # 0 = segunda ... 6 = domingo
print(df[["data", "ano", "mes", "mes_ano", "dia_semana"]].head(3))

# 4) Filtrar por período: compare com uma data (texto ISO 'AAAA-MM-DD' funciona)
agosto = df[(df["data"] >= "2026-08-01") & (df["data"] <= "2026-08-31")]
print("Bobinas medidas em agosto:", len(agosto))

# 5) Diferença entre datas vira Timedelta
ops = pd.read_csv(DADOS / "ops_protheus.csv", sep=";", encoding="cp1252", dtype={"op": str})
ops["emissao"] = pd.to_datetime(ops["emissao"], format="%d/%m/%Y")
primeira_medicao = df.groupby("op", as_index=False)["data"].min()
prazo = ops.merge(primeira_medicao, on="op")
prazo["dias_ate_medir"] = (prazo["data"] - prazo["emissao"]).dt.days
print(prazo[["op", "emissao", "data", "dias_ate_medir"]].head(4))

# 6) Agrupar por mês: to_period("M") transforma a data no "mês dela"
df["periodo"] = df["data"].dt.to_period("M")
print(df.groupby("periodo")["peso_kg"].sum())

# 7) Erro comum: data inválida. errors="coerce" troca por NaT (o NaN das datas).
textos = pd.Series(["15/09/2026", "31/09/2026", ""])
print(pd.to_datetime(textos, format="%d/%m/%Y", errors="coerce"))
