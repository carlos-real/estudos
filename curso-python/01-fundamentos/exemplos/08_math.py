"""Exemplo 08 — o módulo math.

Rode com:  python exemplos/08_math.py
"""

import math

print("pi:", math.pi)
print("Raiz de 144:", math.sqrt(144))
print("Para cima (ceil) 83.1:", math.ceil(83.1))
print("Para baixo (floor) 83.9:", math.floor(83.9))
print("Potência com **:", 2**10)

# Área de um corpo de prova circular (diâmetro de 113 mm, usado em gramatura)
diametro_mm = 113
raio_m = diametro_mm / 1000 / 2
area_m2 = math.pi * raio_m**2
print(f"Área do disco: {area_m2:.5f} m²")

# Quantas caixas para 47 bobinas, se cabem 6 por caixa?
print("Caixas necessárias:", math.ceil(47 / 6))
