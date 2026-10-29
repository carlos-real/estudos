"""
Exercício 10.06 — Limpar medições digitadas à mão (SOLUÇÃO)

Limpeza boa é uma sequência de passos pequenos, um problema por vez, na ordem
certa. A ordem importa: só dá para achar a bobina repetida DEPOIS de padronizar,
e só dá para descartar "sem espessura" DEPOIS de converter "n/d" em ausente.
"""

import pandas as pd


def texto_br_para_numero(coluna: pd.Series) -> pd.Series:
    """'1.120,5' -> 1120.5. O que não for número vira NaN."""
    # regex=False: o "." aqui é um ponto de verdade, não o "qualquer caractere"
    # das expressões regulares (módulo 05).
    sem_milhar = coluna.str.strip().str.replace(".", "", regex=False)
    com_ponto = sem_milhar.str.replace(",", ".", regex=False)
    # errors="coerce": "n/d" e "" viram NaN em vez de levantar ValueError.
    return pd.to_numeric(com_ponto, errors="coerce")


def limpar_medicoes(bruto: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras de limpeza e devolve uma tabela nova."""
    df = bruto.copy()  # nunca mexa na tabela de quem chamou

    # 1. Texto padronizado
    df["linha"] = df["linha"].str.strip().str.upper()

    # 2 e 3. Números. Cuidado: na espessura NÃO há ponto de milhar, mas a mesma
    # função serve, porque "49,8" não tem ponto nenhum para remover.
    df["espessura_um"] = texto_br_para_numero(df["espessura_um"])
    df["peso_kg"] = texto_br_para_numero(df["peso_kg"])

    # 4. Sem espessura não há o que avaliar
    df = df.dropna(subset=["espessura_um"])

    # 5. A primeira ocorrência de cada bobina fica (keep="first" é o padrão)
    df = df.drop_duplicates(subset=["bobina"], keep="first")

    # 6. Índice limpo
    return df.reset_index(drop=True)
