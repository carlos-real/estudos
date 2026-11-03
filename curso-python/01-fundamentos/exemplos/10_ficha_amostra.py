"""Exemplo 10 — No mundo real: ficha de uma amostra de filme.

Rode com:  python exemplos/10_ficha_amostra.py

Os dados chegam como TEXTO (como viriam de uma planilha ou de um formulário),
são limpos, convertidos, calculados e impressos numa ficha formatada.
"""

import math

# --- Dados de entrada (do jeito que chegam) ---
op_digitada = " op-48213 "
linha = "c"
espessura_1 = "24,8"
espessura_2 = "25,3"
espessura_3 = "25,1"
massa_corpo_prova_g = "0,4710"  # disco de 100 cm²
comprimento_bobina_m = 6000
largura_bobina_mm = 640
espessura_nominal_um = 25.0
tolerancia_pct = 8.0

# --- Limpeza e conversão ---
op = "OP" + op_digitada.upper().replace("OP", "").replace("-", "").strip()
linha = linha.strip().upper()
e1 = float(espessura_1.replace(",", "."))
e2 = float(espessura_2.replace(",", "."))
e3 = float(espessura_3.replace(",", "."))
massa_g = float(massa_corpo_prova_g.replace(",", "."))

# --- Cálculos ---
media_um = (e1 + e2 + e3) / 3
minimo_um = espessura_nominal_um - espessura_nominal_um * tolerancia_pct / 100
maximo_um = espessura_nominal_um + espessura_nominal_um * tolerancia_pct / 100
desvio = (media_um - espessura_nominal_um) / espessura_nominal_um
gramatura = massa_g / 0.01  # 100 cm² = 0,01 m²
peso_kg = gramatura * (largura_bobina_mm / 1000) * comprimento_bobina_m / 1000
diametro_mm = math.sqrt(76**2 + 4 * comprimento_bobina_m * 1000 * (media_um / 1000) / math.pi)

# --- Saída ---
faixa = f"{minimo_um:.2f} a {maximo_um:.2f}"
print("=" * 40)
print(f"{'FICHA DE AMOSTRA':^40}")
print("=" * 40)
print(f"{'OP':<22}{op:>18}")
print(f"{'Linha':<22}{linha:>18}")
print(f"{'Espessura média (µm)':<22}{media_um:>18.2f}")
print(f"{'Faixa (µm)':<22}{faixa:>18}")
print(f"{'Desvio do nominal':<22}{desvio:>+18.2%}")
print(f"{'Gramatura (g/m²)':<22}{gramatura:>18.1f}")
print(f"{'Peso estimado (kg)':<22}{peso_kg:>18,.2f}")
print(f"{'Diâmetro estimado (mm)':<22}{diametro_mm:>18.0f}")
print("-" * 40)
print("Veredito: aprovado ou reprovado? No módulo 02!")
