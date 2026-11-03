"""
Exercício 10.04 — Colunas calculadas: desvio e status (SOLUÇÃO)

Duas lições aqui:
1. Conta com coluna vale para todas as linhas de uma vez (vetorização): nada de for.
2. Função que recebe tabela não deve alterar a tabela de quem chamou (efeito
   colateral, módulo 04). Por isso começamos com .copy().
"""

import pandas as pd


def adicionar_desvio(df: pd.DataFrame, nominal: float) -> pd.DataFrame:
    """Nova tabela com as colunas desvio_um e desvio_pct."""
    resultado = df.copy()
    diferenca = resultado["espessura_um"] - nominal  # uma Series inteira
    resultado["desvio_um"] = diferenca.round(2)
    resultado["desvio_pct"] = (diferenca / nominal * 100).round(2)
    return resultado
    # Alternativa sem copy explícito: df.assign(desvio_um=..., desvio_pct=...)
    # assign SEMPRE devolve uma tabela nova.


def classificar(df: pd.DataFrame, tolerancia_pct: float) -> pd.DataFrame:
    """Nova tabela com a coluna status (APROVADA/REPROVADA)."""
    resultado = df.copy()
    # Padrão "valor padrão + exceções": todo mundo começa aprovado e o .loc troca
    # só as linhas em que a máscara é True. Uma linha só, sem atribuição encadeada.
    resultado["status"] = "APROVADA"
    fora = resultado["desvio_pct"].abs() > tolerancia_pct
    resultado.loc[fora, "status"] = "REPROVADA"
    return resultado
    # Alternativa com numpy (vem junto com o pandas):
    #   import numpy as np
    #   resultado["status"] = np.where(fora, "REPROVADA", "APROVADA")
