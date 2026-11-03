"""
Exercício 10.11 — Gráfico de barras: peso por linha (SOLUÇÃO)

Barras servem para COMPARAR categorias (linhas A, B, C, D). O caminho mais curto
é resumir com groupby e chamar .plot.bar() na Series: o pandas desenha com o
matplotlib e devolve o Axes, que é onde configuramos título e rótulos.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes


def grafico_peso_por_linha(df: pd.DataFrame) -> Axes:
    """Barras com o peso total (t) por linha de produção."""
    peso_t = df.groupby("linha")["peso_kg"].sum() / 1000  # groupby já ordena A, B, C...

    # Criar a figura explicitamente evita desenhar por cima de um gráfico antigo.
    fig, ax = plt.subplots()
    peso_t.plot.bar(ax=ax, color="#1F4E78", rot=0)  # rot=0: rótulos na horizontal
    ax.set_title("Peso medido por linha")
    ax.set_xlabel("Linha")
    ax.set_ylabel("Peso (t)")
    fig.tight_layout()  # ajusta margens para nada ficar cortado
    return ax

    # Alternativa só com matplotlib:
    #   ax.bar(peso_t.index, peso_t.values)


def salvar_png(ax: Axes, caminho: str | Path) -> Path:
    """Salva a figura do Axes em PNG e devolve o caminho."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)  # módulo 06: pathlib
    # O Axes mora dentro de uma Figure; quem salva é a figura.
    ax.figure.savefig(caminho, dpi=120)
    return caminho
