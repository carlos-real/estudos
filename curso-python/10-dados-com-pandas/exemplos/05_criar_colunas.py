"""Exemplo 05 — Criar e alterar colunas (e o cuidado com cópias).

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/05_criar_colunas.py
"""

import pandas as pd

df = pd.DataFrame(
    {
        "bobina": ["024447-01", "024447-02", "024447-03", "024447-04"],
        "nominal_um": [62.0, 62.0, 62.0, 62.0],
        "espessura_um": [61.8, 58.9, 67.5, 62.0],
        "peso_kg": [1180.4, 1325.0, 990.7, 1402.3],
    }
)

# 1) Coluna calculada: a conta vale para todas as linhas de uma vez.
df["desvio_pct"] = ((df["espessura_um"] - df["nominal_um"]) / df["nominal_um"] * 100).round(2)
df["peso_t"] = df["peso_kg"] / 1000
print(df)

# 2) Coluna condicional: comece com um valor e troque onde a condição vale.
df["status"] = "APROVADA"
df.loc[df["desvio_pct"].abs() > 7, "status"] = "REPROVADA"
print(df[["bobina", "desvio_pct", "status"]])

# 3) Traduzir códigos com um dicionário: map.
classes = {"APROVADA": "verde", "REPROVADA": "vermelho"}
df["cor"] = df["status"].map(classes)
print(df[["bobina", "status", "cor"]])

# 4) Faixas numéricas: pd.cut corta em intervalos e dá um nome para cada um.
df["faixa_peso"] = pd.cut(
    df["peso_kg"], bins=[0, 1000, 1300, 2000], labels=["leve", "média", "pesada"]
)
print(df[["bobina", "peso_kg", "faixa_peso"]])

# 5) Apagar e renomear colunas: devolvem um DataFrame NOVO.
enxuto = df.drop(columns=["peso_t", "cor"]).rename(columns={"espessura_um": "medido_um"})
print(enxuto.columns.tolist())

# 6) Cópias: filtrou e vai alterar? Use .copy() para deixar claro que é outra tabela.
reprovadas = df[df["status"] == "REPROVADA"].copy()
reprovadas["acao"] = "segregar"
print(reprovadas[["bobina", "acao"]])
print("A tabela original ganhou a coluna 'acao'?", "acao" in df.columns)
