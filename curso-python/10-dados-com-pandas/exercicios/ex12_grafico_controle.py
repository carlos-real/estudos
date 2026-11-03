"""
Exercício 10.12 — Gráfico de controle (média ± 3σ)
Nível: ★★★

Contexto: o laboratório quer acompanhar a espessura de um produto bobina a
bobina. Os limites de controle são calculados num período de REFERÊNCIA, em que
o processo estava estável, e depois usados para vigiar as bobinas novas:
    média = média da referência
    σ     = desvio-padrão amostral da referência
    LIC   = média - 3σ   (limite inferior de controle)
    LSC   = média + 3σ   (limite superior de controle)
Um ponto fora de [LIC, LSC] indica causa especial: vale investigar.

Tarefa: implemente três funções.
  1. limites_de_controle(referencia): recebe uma Series de números e devolve o
     dicionário {"media": ..., "lic": ..., "lsc": ...} (floats, sem arredondar).
     Com menos de 2 valores, levante ValueError (não dá para calcular σ).
  2. pontos_fora_de_controle(valores, limites): devolve a lista das POSIÇÕES
     (0, 1, 2...) dos valores estritamente abaixo do LIC ou acima do LSC.
  3. grafico_controle(valores, limites, titulo): desenha e devolve o Axes com:
       - os valores como linha com marcadores, no eixo x as amostras 1, 2, 3...;
       - três linhas horizontais (ax.axhline): média, LIC e LSC;
       - os pontos fora de controle destacados com ax.scatter (se não houver
         nenhum, não chame o scatter);
       - título = titulo; eixo x "Amostra"; eixo y "Valor".
     O gráfico deve ter exatamente 4 linhas (a dos valores + 3 horizontais).

Exemplos:
    >>> ref = pd.Series([61.8, 62.3, 61.5, 62.0, 62.4])
    >>> limites = limites_de_controle(ref)
    >>> {k: round(v, 2) for k, v in limites.items()}
    {'media': 62.0, 'lic': 60.9, 'lsc': 63.1}
    >>> pontos_fora_de_controle(pd.Series([62.1, 63.5, 61.9, 60.0]), limites)
    [1, 3]

Dica: .std() do pandas já é o amostral; posições: range(len(valores)) ou
.reset_index(drop=True) e o índice; fig, ax = plt.subplots().

Teste com:  python curso.py testar 10 ex12
"""

import matplotlib.pyplot as plt  # noqa: F401  (pode ser útil: plt.subplots)
import pandas as pd
from matplotlib.axes import Axes


def limites_de_controle(referencia: pd.Series) -> dict[str, float]:
    """Média, LIC e LSC (média ± 3 desvios-padrão amostrais)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def pontos_fora_de_controle(valores: pd.Series, limites: dict[str, float]) -> list[int]:
    """Posições dos valores fora de [LIC, LSC]."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def grafico_controle(valores: pd.Series, limites: dict[str, float], titulo: str) -> Axes:
    """Desenha o gráfico de controle e devolve o Axes."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
