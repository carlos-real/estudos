"""
Exercício 10.12 — Gráfico de controle (SOLUÇÃO)

Por que calcular os limites numa REFERÊNCIA e não nos próprios dados vigiados?
Porque um ponto muito fora puxa a média e infla o σ, alargando os limites justo
quando deveria aparecer. Com poucos pontos, isso é pior ainda: com 10 valores,
nenhum consegue ficar a mais de 3σ da média calculada com ele mesmo.
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes


def limites_de_controle(referencia: pd.Series) -> dict[str, float]:
    """Média, LIC e LSC (média ± 3 desvios-padrão amostrais)."""
    if len(referencia) < 2:
        raise ValueError("são precisos pelo menos 2 valores para calcular o desvio-padrão")
    media = float(referencia.mean())
    sigma = float(referencia.std())  # amostral (ddof=1), igual ao DESVPAD do Excel
    return {"media": media, "lic": media - 3 * sigma, "lsc": media + 3 * sigma}


def pontos_fora_de_controle(valores: pd.Series, limites: dict[str, float]) -> list[int]:
    """Posições dos valores fora de [LIC, LSC]."""
    # reset_index(drop=True) troca os rótulos por posições 0, 1, 2... Assim a
    # função funciona mesmo que a Series venha de um filtro (índice 7, 12, 40...).
    v = valores.reset_index(drop=True)
    fora = (v < limites["lic"]) | (v > limites["lsc"])
    return v.index[fora].tolist()


def grafico_controle(valores: pd.Series, limites: dict[str, float], titulo: str) -> Axes:
    """Desenha o gráfico de controle e devolve o Axes."""
    v = valores.reset_index(drop=True)
    x = range(1, len(v) + 1)  # amostras numeradas a partir de 1, como no laboratório

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, v, marker="o", color="#1F4E78", label="Valores")
    ax.axhline(limites["media"], color="green", label="Média")
    ax.axhline(limites["lsc"], color="red", linestyle="--", label="LSC")
    ax.axhline(limites["lic"], color="red", linestyle="--", label="LIC")

    fora = pontos_fora_de_controle(v, limites)
    if fora:
        # x da posição p é p + 1 (a numeração do gráfico começa em 1)
        ax.scatter([p + 1 for p in fora], v[fora], color="red", s=80, zorder=3)

    ax.set_title(titulo)
    ax.set_xlabel("Amostra")
    ax.set_ylabel("Valor")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    return ax
