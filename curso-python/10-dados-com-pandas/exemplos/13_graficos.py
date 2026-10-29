"""Exemplo 13 — Gráficos com matplotlib: barras, linhas, histograma e dispersão.

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/13_graficos.py            # só salva os PNG
    python 10-dados-com-pandas/exemplos/13_graficos.py --mostrar  # salva e abre as janelas

Os PNG vão para 10-dados-com-pandas/saida/.
"""

import sys
from pathlib import Path

import matplotlib

if "--mostrar" not in sys.argv:
    matplotlib.use("Agg")  # só desenha em arquivo, sem abrir janela

import matplotlib.pyplot as plt
import pandas as pd

PASTA_MODULO = Path(__file__).resolve().parent.parent
SAIDA = PASTA_MODULO / "saida"
SAIDA.mkdir(exist_ok=True)

df = pd.read_csv(
    PASTA_MODULO / "dados" / "medicoes.csv",
    sep=";",
    decimal=",",
    thousands=".",
    dtype={"op": str},
)
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

# 1) BARRAS: comparar categorias. "Quanto cada linha produziu?"
peso_t = df.groupby("linha")["peso_kg"].sum() / 1000
ax = peso_t.plot.bar(color="#1F4E78", rot=0)  # DataFrame/Series.plot devolve um Axes
ax.set_title("Peso medido por linha (jul–set/2026)")
ax.set_xlabel("Linha")
ax.set_ylabel("Peso (t)")
ax.figure.tight_layout()
ax.figure.savefig(SAIDA / "barras_peso_por_linha.png", dpi=120)
print("Barras desenhadas:", len(ax.patches))

# 2) LINHAS: evolução no tempo. "A produção está subindo ou caindo?"
#    Aqui usamos o pyplot direto: fig (a folha) e ax (o gráfico dentro dela).
semanal = df.set_index("data").resample("W")["peso_kg"].sum() / 1000
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(semanal.index, semanal.values, marker="o")
ax.set_title("Peso medido por semana")
ax.set_xlabel("Semana")
ax.set_ylabel("Peso (t)")
ax.grid(alpha=0.3)
fig.autofmt_xdate()  # inclina as datas para não encavalarem
fig.tight_layout()
fig.savefig(SAIDA / "linhas_peso_semanal.png", dpi=120)
print("Pontos na linha:", len(ax.get_lines()[0].get_xdata()))

# 3) HISTOGRAMA: distribuição de uma medida. "Como as espessuras se espalham?"
lam = df[df["produto"] == "LAM-62"]
fig, ax = plt.subplots()
ax.hist(lam["espessura_um"], bins=6, color="#7FA7C9", edgecolor="black")
ax.axvline(62, color="green", linestyle="--", label="Nominal 62 µm")
ax.set_title("Espessura do LAM-62")
ax.set_xlabel("Espessura (µm)")
ax.set_ylabel("Nº de bobinas")
ax.legend()
fig.tight_layout()
fig.savefig(SAIDA / "histograma_lam62.png", dpi=120)

# 4) DISPERSÃO: relação entre duas medidas. "Mais espesso = mais gramatura?"
ax = df.plot.scatter(x="espessura_um", y="gramatura_gm2", alpha=0.7)
ax.set_title("Espessura x gramatura")
ax.set_xlabel("Espessura (µm)")
ax.set_ylabel("Gramatura (g/m²)")
ax.figure.tight_layout()
ax.figure.savefig(SAIDA / "dispersao_esp_gram.png", dpi=120)
print("Correlação espessura x gramatura:", round(df["espessura_um"].corr(df["gramatura_gm2"]), 3))

if "--mostrar" in sys.argv:
    plt.show()
plt.close("all")
print("PNG salvos em", SAIDA.name + "/")
