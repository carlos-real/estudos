"""statistics no laboratório: média, mediana, desvio padrão e CV%.

Rode com:  python exemplos/08_estatistica_lab.py
"""

import statistics

espessuras = [25.1, 24.8, 25.3, 24.9, 25.4, 25.0]  # µm, 6 pontos da bobina

media = statistics.mean(espessuras)
mediana = statistics.median(espessuras)
desvio = statistics.stdev(espessuras)  # amostral (n - 1) = DESVPAD.A do Excel
desvio_pop = statistics.pstdev(espessuras)  # populacional (n) = DESVPAD.P do Excel
cv = desvio / media * 100

print(f"n = {len(espessuras)}")
print(f"Média   = {media:.3f} µm")
print(f"Mediana = {mediana:.3f} µm")
print(f"Desvio  = {desvio:.3f} µm (amostral)")
print(f"Desvio  = {desvio_pop:.3f} µm (populacional)")
print(f"CV      = {cv:.2f} %")
print(f"Amplitude = {max(espessuras) - min(espessuras):.1f} µm")

# Mediana resiste a valor estranho; média não
com_erro = espessuras + [52.0]  # alguém digitou 52 em vez de 25,2
print(f"\nCom erro de digitação: média {statistics.mean(com_erro):.2f}", end="")
print(f" | mediana {statistics.median(com_erro):.2f}")

# Quartis (útil para achar valores fora do padrão)
quartis = statistics.quantiles(espessuras, n=4)
print("Quartis:", [round(q, 3) for q in quartis])

try:
    statistics.stdev([25.1])
except statistics.StatisticsError as erro:
    print("Erro esperado:", erro)
