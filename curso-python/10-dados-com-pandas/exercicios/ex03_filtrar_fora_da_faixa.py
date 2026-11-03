"""
Exercício 10.03 — Filtrar o que está fora da faixa
Nível: ★☆☆

Contexto: antes de liberar uma série, o laboratório quer ver só as bobinas com
alguma medida fora da faixa, e às vezes só as de algumas linhas.

Tarefa: implemente duas funções. Nenhuma pode alterar o DataFrame recebido.
  1. fora_da_faixa(df, coluna, minimo, maximo): devolve as linhas em que o valor
     da coluna é MENOR que o mínimo ou MAIOR que o máximo (os limites em si estão
     dentro da faixa). Mantenha a ordem original e renumere o índice (0, 1, 2...).
  2. filtrar_linhas(df, linhas): devolve as linhas cuja coluna "linha" está na
     lista recebida (ex.: ["A", "C"]), na ordem original e com índice 0, 1, 2...

Exemplos:
    >>> df
          bobina linha  espessura_um
    0  024412-01     A          38.1
    1  024412-02     A          44.5
    2  024413-01     B          35.0
    >>> fora_da_faixa(df, "espessura_um", 36.0, 44.0)
          bobina linha  espessura_um
    0  024412-02     A          44.5
    >>> filtrar_linhas(df, ["B"])
          bobina linha  espessura_um
    0  024413-01     B          35.0

Dica: máscara booleana com | (ou) e parênteses, ou ~ com .between(); .isin()
para "está na lista"; .reset_index(drop=True) para renumerar.

Teste com:  python curso.py testar 10 ex03
"""

import pandas as pd


def fora_da_faixa(df: pd.DataFrame, coluna: str, minimo: float, maximo: float) -> pd.DataFrame:
    """Linhas com valor abaixo do mínimo ou acima do máximo."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def filtrar_linhas(df: pd.DataFrame, linhas: list[str]) -> pd.DataFrame:
    """Linhas cuja coluna 'linha' está na lista."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
