"""
Exercício 10.11 — Gráfico de barras: peso por linha
Nível: ★☆☆

Contexto: o gerente da produção quer, no relatório mensal, um gráfico simples
com o peso total medido em cada linha de produção, em toneladas.

Tarefa: implemente duas funções.
  1. grafico_peso_por_linha(df): a tabela tem as colunas "linha" e "peso_kg".
     Desenhe um gráfico de BARRAS com uma barra por linha de produção (em ordem
     alfabética), altura = soma do peso em TONELADAS (kg / 1000). Configure:
       título:  "Peso medido por linha"
       eixo x:  "Linha"
       eixo y:  "Peso (t)"
     Devolva o objeto Axes (o "gráfico" do matplotlib).
  2. salvar_png(ax, caminho): salva a figura do Axes em PNG no caminho dado,
     criando a pasta se ela não existir. Devolve o caminho como Path.

Exemplo:
    >>> ax = grafico_peso_por_linha(df)
    >>> ax.get_title()
    'Peso medido por linha'
    >>> [barra.get_height() for barra in ax.patches]
    [33.1238, 18.5435, 12.4077, 21.0468]
    >>> salvar_png(ax, Path("saida/peso.png"))
    PosixPath('saida/peso.png')      (no Windows aparece WindowsPath)

Dica: (df.groupby("linha")["peso_kg"].sum() / 1000).plot.bar() devolve o Axes;
ax.set_title, ax.set_xlabel, ax.set_ylabel; ax.figure.savefig(caminho).

Teste com:  python curso.py testar 10 ex11
"""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401  (pode ser útil: plt.subplots)
import pandas as pd
from matplotlib.axes import Axes


def grafico_peso_por_linha(df: pd.DataFrame) -> Axes:
    """Barras com o peso total (t) por linha de produção."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def salvar_png(ax: Axes, caminho: str | Path) -> Path:
    """Salva a figura do Axes em PNG e devolve o caminho."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
