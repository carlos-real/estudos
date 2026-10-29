"""
Exercício 10.01 — Primeiro DataFrame
Nível: ★☆☆

Contexto: a expedição mandou duas listas soltas: o código de cada bobina e o
peso dela. Você quer transformar isso numa tabela para fazer contas.

Tarefa: implemente três funções.
  1. criar_tabela_bobinas(bobinas, pesos): devolve um DataFrame com as colunas
     "bobina" e "peso_kg", nessa ordem. Se as listas tiverem tamanhos
     diferentes, levante ValueError.
  2. peso_total(tabela): soma da coluna "peso_kg" como float. Tabela vazia -> 0.0.
  3. bobina_mais_pesada(tabela): o código (texto) da bobina de maior peso. Se
     houver empate, vale a que aparece primeiro.

Exemplos:
    >>> tabela = criar_tabela_bobinas(["024412-01", "024412-02"], [1250.5, 980.0])
    >>> tabela
          bobina  peso_kg
    0  024412-01   1250.5
    1  024412-02    980.0
    >>> peso_total(tabela)
    2230.5
    >>> bobina_mais_pesada(tabela)
    '024412-01'

Dica: pd.DataFrame({"coluna": lista, ...}); a Series tem .sum() e .idxmax()
(o rótulo da linha do maior valor), e .loc[rótulo, "coluna"] pega um valor.

Teste com:  python curso.py testar 10 ex01
"""

import pandas as pd


def criar_tabela_bobinas(bobinas: list[str], pesos: list[float]) -> pd.DataFrame:
    """Monta a tabela com as colunas 'bobina' e 'peso_kg'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_total(tabela: pd.DataFrame) -> float:
    """Soma da coluna 'peso_kg' (0.0 se a tabela estiver vazia)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def bobina_mais_pesada(tabela: pd.DataFrame) -> str:
    """Código da bobina de maior peso (a primeira, em caso de empate)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
