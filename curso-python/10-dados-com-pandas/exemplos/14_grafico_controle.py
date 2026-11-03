"""Exemplo 14 — Gráfico de controle simples (valores individuais, média ± 3σ).

Rode (na pasta curso-python):
    python 10-dados-com-pandas/exemplos/14_grafico_controle.py            # só salva o PNG
    python 10-dados-com-pandas/exemplos/14_grafico_controle.py --mostrar  # salva e abre
"""

import sys
from pathlib import Path

import matplotlib

if "--mostrar" not in sys.argv:
    matplotlib.use("Agg")

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

# Espessura do LAM-62, na ordem em que as bobinas foram medidas
lam = df[df["produto"] == "LAM-62"].sort_values(["data", "bobina"]).reset_index(drop=True)
valores = lam["espessura_um"]

# 1) Limites de controle: média ± 3 desvios-padrão (a "voz do processo")
media = valores.mean()
sigma = valores.std()  # desvio-padrão amostral (ddof=1), igual ao DESVPAD do Excel
lsc = media + 3 * sigma  # limite superior de controle
lic = media - 3 * sigma  # limite inferior de controle
print(f"Média {media:.2f} | σ {sigma:.2f} | LIC {lic:.2f} | LSC {lsc:.2f}")

# 2) Limites de especificação: 62 µm ± 7% (a "voz do cliente")
lie, lse = 62 * 0.93, 62 * 1.07
fora_controle = valores[(valores > lsc) | (valores < lic)]
fora_especificacao = valores[(valores > lse) | (valores < lie)]
print("Pontos fora de CONTROLE:", len(fora_controle))
print("Pontos fora de ESPECIFICAÇÃO:", fora_especificacao.tolist())

# 3) O gráfico
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(valores.index + 1, valores, marker="o", color="#1F4E78", label="Espessura")
ax.axhline(media, color="green", label=f"Média {media:.1f}")
ax.axhline(lsc, color="red", linestyle="--", label=f"LSC {lsc:.1f}")
ax.axhline(lic, color="red", linestyle="--", label=f"LIC {lic:.1f}")
ax.axhline(lse, color="orange", linestyle=":", label=f"LSE {lse:.2f}")
ax.axhline(lie, color="orange", linestyle=":", label=f"LIE {lie:.2f}")
ax.scatter(fora_especificacao.index + 1, fora_especificacao, color="orange", s=90, zorder=3)
ax.set_title("Gráfico de controle — espessura LAM-62 (linha D)")
ax.set_xlabel("Bobina (ordem de medição)")
ax.set_ylabel("Espessura (µm)")
ax.legend(loc="lower right", fontsize=8, ncols=3)
fig.tight_layout()
fig.savefig(SAIDA / "controle_lam62.png", dpi=120)
print("Linhas no gráfico:", len(ax.get_lines()))

if "--mostrar" in sys.argv:
    plt.show()
plt.close("all")
