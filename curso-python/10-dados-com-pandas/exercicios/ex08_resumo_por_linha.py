"""
Exercício 10.08 — Resumo por linha de produção
Nível: ★★☆

Contexto: na reunião mensal, a qualidade apresenta um quadro por linha: quantas
bobinas foram medidas, o peso total, a espessura média e a variação dela.

Tarefa: implemente resumo_por_linha(df). A tabela recebida tem as colunas
"linha", "bobina", "espessura_um", "peso_kg" e "cof". Devolva um DataFrame com
UMA linha por linha de produção, em ordem alfabética, índice 0, 1, 2... e as
colunas, nesta ordem:
  - "linha"
  - "bobinas":          quantidade de bobinas
  - "peso_total_kg":    soma de peso_kg, 1 casa decimal
  - "espessura_media":  média de espessura_um, 2 casas
  - "espessura_desvio": desvio-padrão amostral de espessura_um, 2 casas
                        (linha com uma bobina só fica com NaN, e tudo bem)
  - "cof_max":          maior COF

Exemplo:
    >>> resumo_por_linha(df)
      linha  bobinas  peso_total_kg  espessura_media  espessura_desvio  cof_max
    0     A        3         3330.5            39.37              1.17     0.27
    1     B        1         1310.2            35.30               NaN     0.37

Dica: df.groupby("linha", as_index=False).agg(nome=("coluna", "função"), ...)
e depois .round({...}) com um dicionário {coluna: casas}.

Teste com:  python curso.py testar 10 ex08
"""

import pandas as pd


def resumo_por_linha(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha de resumo por linha de produção."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
