"""
Exercício 10.06 — Limpar medições digitadas à mão
Nível: ★★☆

Contexto: uma planilha preenchida por várias pessoas chegou bagunçada: linha
escrita como " a" ou "B ", números com vírgula guardados como texto, "n/d" no
lugar da medida e a mesma bobina lançada duas vezes.

Tarefa: implemente limpar_medicoes(bruto). A tabela recebida tem as colunas
"op", "linha", "bobina", "espessura_um" e "peso_kg", TODAS como texto (foi lida
com dtype=str, então células vazias chegam como ausentes). Devolva uma tabela
NOVA, com as mesmas colunas, aplicando as regras nesta ordem:
  1. "linha": sem espaços nas pontas e em maiúscula (" a" -> "A").
  2. "espessura_um": texto com vírgula decimal vira número ("49,8" -> 49.8,
     " 34,7 " -> 34.7). O que não for número ("n/d", vazio) vira ausente (NaN).
  3. "peso_kg": formato brasileiro com milhar ("1.120,5" -> 1120.5); vazio fica
     ausente (NaN), sem descartar a linha.
  4. Descarte as linhas sem espessura (não dá para avaliar sem medida).
  5. Se a mesma "bobina" aparecer mais de uma vez, fique só com a primeira.
  6. Índice renumerado: 0, 1, 2, ...
Não altere a tabela recebida.

Exemplo:
    >>> bruto
           op linha     bobina espessura_um  peso_kg
    0  024470     A  024470-01         51,2  1.120,5
    1  024470    a   024470-02          n/d  1.098,0
    >>> limpar_medicoes(bruto)
           op linha     bobina  espessura_um  peso_kg
    0  024470     A  024470-01          51.2   1120.5

Dica: .str.strip(), .str.upper(), .str.replace(".", "", regex=False),
pd.to_numeric(..., errors="coerce"), .dropna(subset=[...]),
.drop_duplicates(subset=[...]).

Teste com:  python curso.py testar 10 ex06
"""

import pandas as pd


def limpar_medicoes(bruto: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras de limpeza e devolve uma tabela nova."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
