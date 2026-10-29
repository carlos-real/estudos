"""
Exercício 10.10 — Datas e tabela dinâmica (SOLUÇÃO)

Por que o mês como TEXTO "AAAA-MM"? Porque texto nesse formato ordena certo
(2026-09 < 2026-10) e vira um cabeçalho de coluna legível. Formato "MM/AAAA"
ordenaria errado: "01/2027" viria antes de "12/2026".
"""

import pandas as pd


def adicionar_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Nova tabela com a coluna 'mes' (AAAA-MM) calculada da coluna 'data'."""
    resultado = df.copy()
    # format explícito: "03/07/2026" é 3 de julho, nunca 7 de março.
    # Sem errors="coerce", data inválida ("31/09/2026") ou vazia levanta
    # ValueError, que é exatamente o que o enunciado pede: melhor parar do que
    # somar peso no mês errado.
    datas = pd.to_datetime(resultado["data"], format="%d/%m/%Y")
    if datas.isna().any():  # células vazias (None/NaN) viram NaT sem erro
        raise ValueError("há datas vazias na tabela")
    resultado["mes"] = datas.dt.strftime("%Y-%m")
    return resultado


def peso_por_linha_e_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Tabela dinâmica: linhas x meses, soma do peso."""
    com_mes = adicionar_mes(df)  # reaproveita a função de cima
    tabela = com_mes.pivot_table(
        index="linha",
        columns="mes",
        values="peso_kg",
        aggfunc="sum",
        fill_value=0.0,  # linha que não produziu no mês: 0, não NaN
    )
    # pivot_table já ordena índice e colunas e dá os nomes "linha" e "mes".
    return tabela.round(1)
