"""
Exercício 10.10 — Datas e tabela dinâmica: peso por linha e mês
Nível: ★★☆

Contexto: o PCP pediu uma tabela com o peso medido por linha (nas linhas da
tabela) e por mês (nas colunas), igual à tabela dinâmica que fazem no Excel.

Tarefa: implemente duas funções.
  1. adicionar_mes(df): a coluna "data" tem texto no formato dd/mm/aaaa
     ("03/07/2026"). Devolva uma tabela NOVA com a coluna "mes" no formato
     "AAAA-MM" ("2026-07"). Data inválida ou vazia -> ValueError.
  2. peso_por_linha_e_mes(df): recebe uma tabela com "linha", "data" e
     "peso_kg" e devolve a tabela dinâmica:
       - índice: as linhas de produção (nome do índice: "linha"), em ordem;
       - colunas: os meses "AAAA-MM" em ordem (nome das colunas: "mes");
       - valores: soma do peso_kg, 1 casa decimal; combinação sem
         produção = 0.0.

Exemplo:
    >>> df
      linha        data  peso_kg
    0     A  03/07/2026   1558.5
    1     A  15/08/2026    980.0
    2     B  20/07/2026   1310.2
    >>> peso_por_linha_e_mes(df)
    mes    2026-07  2026-08
    linha
    A       1558.5    980.0
    B       1310.2      0.0

Dica: pd.to_datetime(..., format="%d/%m/%Y") levanta ValueError sozinho quando
a data não bate com o formato; .dt.strftime("%Y-%m") formata; pivot_table tem
index, columns, values, aggfunc e fill_value.

Teste com:  python curso.py testar 10 ex10
"""

import pandas as pd


def adicionar_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Nova tabela com a coluna 'mes' (AAAA-MM) calculada da coluna 'data'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_por_linha_e_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Tabela dinâmica: linhas x meses, soma do peso."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
