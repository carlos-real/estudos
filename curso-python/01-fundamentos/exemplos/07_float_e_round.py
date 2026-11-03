"""Exemplo 07 — o problema do float e o round().

Rode com:  python exemplos/07_float_e_round.py
"""

import math

print("0.1 + 0.2 =", 0.1 + 0.2)
print("1.1 * 3 =", 1.1 * 3)
print("Arredondado:", round(0.1 + 0.2, 2))

# round(x) sem casas devolve int; round(x, n) devolve float
print(round(25.67), round(25.67, 1))

# Arredondamento "do banqueiro": empate (.5) vai para o PAR mais próximo
print("round(2.5) =", round(2.5), "| round(3.5) =", round(3.5))

# 2.675 na verdade é guardado como 2.67499999... no computador
print("round(2.675, 2) =", round(2.675, 2))

# Para comparar floats, use math.isclose
print("isclose(0.1 + 0.2, 0.3):", math.isclose(0.1 + 0.2, 0.3))
