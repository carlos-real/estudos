"""
Exercício 10.08 — Resumo por linha de produção (SOLUÇÃO)

groupby = "separe por grupo, aplique a conta, junte os resultados".
A agregação nomeada (nome_novo=(coluna, função)) já entrega as colunas com os
nomes do relatório, sem precisar renomear depois.
"""

import pandas as pd


def resumo_por_linha(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha de resumo por linha de produção."""
    resumo = df.groupby("linha", as_index=False).agg(
        bobinas=("bobina", "count"),
        peso_total_kg=("peso_kg", "sum"),
        espessura_media=("espessura_um", "mean"),
        espessura_desvio=("espessura_um", "std"),  # std do pandas é amostral (ddof=1)
        cof_max=("cof", "max"),
    )
    # as_index=False deixa "linha" como coluna comum e o índice 0, 1, 2...
    # groupby já ordena as chaves (sort=True é o padrão).
    # round com dicionário: casas diferentes para cada coluna.
    return resumo.round({"peso_total_kg": 1, "espessura_media": 2, "espessura_desvio": 2})

    # Alternativa: groupby("linha").agg(...).reset_index()  -> mesmo resultado.
    # "count" conta valores não ausentes da coluna; "size" contaria linhas.
