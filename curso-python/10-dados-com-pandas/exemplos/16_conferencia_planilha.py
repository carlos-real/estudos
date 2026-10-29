"""Exemplo 16 — No mundo real: conferir a planilha de 4 abas contra as especificações.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/16_conferencia_planilha.py
"""

from pathlib import Path

import pandas as pd

PASTA_MODULO = Path(__file__).resolve().parent.parent
DADOS = PASTA_MODULO / "dados"

NOMES = {
    "OP": "op",
    "Bobina": "bobina",
    "Data": "data",
    "Espessura (µm)": "espessura_um",
    "Gramatura (g/m²)": "gramatura_gm2",
    "COF": "cof",
    "Peso (kg)": "peso_kg",
    "Observação": "observacao",
}


def ler_planilha(caminho: Path) -> pd.DataFrame:
    """Lê todas as abas e devolve uma tabela só, com a coluna 'linha'."""
    abas = pd.read_excel(caminho, sheet_name=None, header=1, dtype={"OP": str})
    partes = [t.assign(linha=nome.removeprefix("Linha ")) for nome, t in abas.items()]
    return pd.concat(partes, ignore_index=True).rename(columns=NOMES)


def produto_da_op(caminho_ops: Path) -> pd.DataFrame:
    ops = pd.read_csv(caminho_ops, sep=";", encoding="cp1252", dtype={"op": str})
    return ops[["op", "produto", "cliente"]]


def conferir(medicoes: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta as colunas 'status' e 'motivo' a cada bobina."""
    df = medicoes.merge(specs, on="produto", how="left")
    folga = df["espessura_nominal"] * df["tolerancia_pct"] / 100
    esp_fora = ~df["espessura_um"].between(
        df["espessura_nominal"] - folga, df["espessura_nominal"] + folga
    )
    folga_g = df["gramatura_nominal"] * df["tolerancia_pct"] / 100
    gram_fora = ~df["gramatura_gm2"].between(
        df["gramatura_nominal"] - folga_g, df["gramatura_nominal"] + folga_g
    )
    cof_fora = df["cof"] > df["cof_max"]
    cof_liberado = df["observacao"].fillna("").str.contains("cof: liberado", case=False)

    df["motivo"] = ""
    df.loc[esp_fora, "motivo"] += "espessura; "
    df.loc[gram_fora, "motivo"] += "gramatura; "
    df.loc[cof_fora & ~cof_liberado, "motivo"] += "COF; "
    df["motivo"] = df["motivo"].str.rstrip("; ")

    df["status"] = "APROVADA"
    df.loc[df["motivo"] != "", "status"] = "REPROVADA"
    df.loc[df["espessura_nominal"].isna(), ["status", "motivo"]] = [
        "PENDENTE",
        "produto sem especificação",
    ]
    df.loc[(df["op"].notna()) & (df["produto"].isna()), ["status", "motivo"]] = [
        "PENDENTE",
        "OP sem cadastro no ERP",
    ]
    return df


medicoes = ler_planilha(DADOS / "planilha_linhas.xlsx")
medicoes = medicoes.merge(produto_da_op(DADOS / "ops_protheus.csv"), on="op", how="left")
specs = pd.read_csv(DADOS / "especificacoes.csv", sep=";", decimal=",")
resultado = conferir(medicoes, specs)

print(resultado["status"].value_counts())
problemas = resultado[resultado["status"] != "APROVADA"]
print(problemas[["linha", "bobina", "status", "motivo"]].to_string(index=False))

resumo = resultado.groupby("linha").agg(
    bobinas=("bobina", "count"),
    aprovadas=("status", lambda s: (s == "APROVADA").sum()),
)
resumo["pct_aprovadas"] = (resumo["aprovadas"] / resumo["bobinas"] * 100).round(1)
print(resumo)
