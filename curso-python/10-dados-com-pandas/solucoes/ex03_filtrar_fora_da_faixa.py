"""
Exercício 10.03 — Filtrar o que está fora da faixa (SOLUÇÃO)

Filtro no pandas = máscara booleana (uma Series de True/False do tamanho da
tabela) dentro de colchetes. O DataFrame original não muda: o filtro devolve
uma tabela nova.
"""

import pandas as pd


def fora_da_faixa(df: pd.DataFrame, coluna: str, minimo: float, maximo: float) -> pd.DataFrame:
    """Linhas com valor abaixo do mínimo ou acima do máximo."""
    valores = df[coluna]
    # Cada comparação vira uma máscara. "|" é o OU elemento a elemento.
    # Os parênteses são obrigatórios: "|" tem precedência maior que "<" e ">".
    mascara = (valores < minimo) | (valores > maximo)
    # Alternativa equivalente: mascara = ~valores.between(minimo, maximo)
    # (between inclui as pontas; o ~ inverte: "não está entre").
    return df[mascara].reset_index(drop=True)


def filtrar_linhas(df: pd.DataFrame, linhas: list[str]) -> pd.DataFrame:
    """Linhas cuja coluna 'linha' está na lista."""
    # isin é o "in" do Python aplicado à coluna inteira de uma vez.
    # drop=True descarta o índice antigo em vez de transformá-lo em coluna.
    return df[df["linha"].isin(linhas)].reset_index(drop=True)
