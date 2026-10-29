"""
Exercício 10.02 — Ler CSV brasileiro
Nível: ★☆☆

Contexto: o laboratório salva as medições pelo Excel em português (CSV com ponto
e vírgula, vírgula decimal e ponto de milhar). As OPs vêm do ERP, num CSV
antigo em cp1252. Ler errado faz o 024412 virar 24412 e o 1.558,5 virar texto.

Tarefa: implemente duas funções.
  1. ler_medicoes(caminho): lê um CSV com separador ";", vírgula decimal,
     ponto de milhar e encoding "utf-8-sig". A coluna "op" deve continuar texto
     (com os zeros à esquerda). Devolve o DataFrame.
  2. ler_ops_erp(caminho): lê o CSV do ERP: separador ";", encoding "cp1252",
     vírgula decimal, ponto de milhar e a coluna "op" como texto.

Exemplo de arquivo de medições:
    data;op;bobina;espessura_um;peso_kg
    03/07/2026;024412;024412-01;38,1;1.558,5

Exemplos:
    >>> df = ler_medicoes("medicoes.csv")
    >>> df.loc[0, "op"], df.loc[0, "espessura_um"], df.loc[0, "peso_kg"]
    ('024412', 38.1, 1558.5)

Dica: pd.read_csv tem os parâmetros sep, decimal, thousands, encoding e dtype.

Teste com:  python curso.py testar 10 ex02
"""

from pathlib import Path

import pandas as pd


def ler_medicoes(caminho: str | Path) -> pd.DataFrame:
    """Lê o CSV de medições no padrão do Excel brasileiro."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ler_ops_erp(caminho: str | Path) -> pd.DataFrame:
    """Lê o CSV de OPs exportado do ERP (cp1252)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
