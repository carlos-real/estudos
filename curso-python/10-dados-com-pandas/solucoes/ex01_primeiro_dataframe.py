"""
Exercício 10.01 — Primeiro DataFrame (SOLUÇÃO)

Ideia central: um DataFrame é um dicionário de colunas. Cada chave vira o nome
da coluna e cada lista vira os valores dela.
"""

import pandas as pd


def criar_tabela_bobinas(bobinas: list[str], pesos: list[float]) -> pd.DataFrame:
    """Monta a tabela com as colunas 'bobina' e 'peso_kg'."""
    # O próprio pandas já recusa listas de tamanhos diferentes com ValueError,
    # mas conferir antes deixa a mensagem clara para quem usa a função.
    if len(bobinas) != len(pesos):
        raise ValueError(f"{len(bobinas)} bobinas para {len(pesos)} pesos")
    # A ordem das chaves do dicionário define a ordem das colunas.
    return pd.DataFrame({"bobina": bobinas, "peso_kg": pesos})


def peso_total(tabela: pd.DataFrame) -> float:
    """Soma da coluna 'peso_kg' (0.0 se a tabela estiver vazia)."""
    # .sum() de uma coluna vazia já dá 0. O float() garante o tipo do Python
    # (o pandas devolve um número do numpy, que se comporta igual, mas é outro tipo).
    return float(tabela["peso_kg"].sum())


def bobina_mais_pesada(tabela: pd.DataFrame) -> str:
    """Código da bobina de maior peso (a primeira, em caso de empate)."""
    # idxmax devolve o RÓTULO (índice) da linha com o maior valor; em empate,
    # devolve o primeiro. Com o rótulo, o .loc busca a bobina daquela linha.
    rotulo = tabela["peso_kg"].idxmax()
    return tabela.loc[rotulo, "bobina"]
    # Alternativa: tabela.sort_values("peso_kg", ascending=False, kind="stable")
    #                     .iloc[0]["bobina"]  (ordena tudo só para pegar um: mais lento)
