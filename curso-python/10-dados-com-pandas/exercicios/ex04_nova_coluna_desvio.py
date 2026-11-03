"""
Exercício 10.04 — Colunas calculadas: desvio e status
Nível: ★☆☆

Contexto: a espessura nominal do produto é 62 µm, com tolerância de ±7%. Você
quer ver, bobina a bobina, quanto cada uma desviou do nominal e se passou.

Tarefa: implemente duas funções. As duas devolvem um DataFrame NOVO e não
podem alterar o DataFrame recebido.
  1. adicionar_desvio(df, nominal): acrescenta as colunas
       "desvio_um"  = espessura_um - nominal              (2 casas decimais)
       "desvio_pct" = (espessura_um - nominal) / nominal * 100  (2 casas)
  2. classificar(df, tolerancia_pct): recebe uma tabela que já tem
     "desvio_pct" e acrescenta "status": "APROVADA" se o desvio, em valor
     absoluto, for <= tolerancia_pct; senão "REPROVADA".

Exemplos:
    >>> df = pd.DataFrame({"bobina": ["01", "02"], "espessura_um": [61.8, 67.5]})
    >>> com_desvio = adicionar_desvio(df, 62.0)
    >>> com_desvio
      bobina  espessura_um  desvio_um  desvio_pct
    0     01          61.8      -0.20       -0.32
    1     02          67.5       5.50        8.87
    >>> classificar(com_desvio, 7.0)["status"].tolist()
    ['APROVADA', 'REPROVADA']

Dica: comece com resultado = df.copy(); contas com colunas são vetorizadas;
.round(2) e .abs() funcionam na coluna inteira; para o status, crie a coluna com
um valor e troque com .loc[mascara, "status"] = "...".

Teste com:  python curso.py testar 10 ex04
"""

import pandas as pd


def adicionar_desvio(df: pd.DataFrame, nominal: float) -> pd.DataFrame:
    """Nova tabela com as colunas desvio_um e desvio_pct."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def classificar(df: pd.DataFrame, tolerancia_pct: float) -> pd.DataFrame:
    """Nova tabela com a coluna status (APROVADA/REPROVADA)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
