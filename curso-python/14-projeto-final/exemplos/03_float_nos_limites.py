"""O float no limite da tolerância: por que os limites são arredondados.

Rode:  python exemplos/03_float_nos_limites.py
"""

nominal, percentual, medido = 37.0, 10, 33.3  # gramatura exatamente no limite

minimo_cru = nominal * (1 - percentual / 100)
print("mínimo calculado:", minimo_cru)
print("33.3 passa sem arredondar?", minimo_cru <= medido)

minimo = round(minimo_cru, 4)
print("mínimo arredondado:", minimo)
print("33.3 passa arredondando?", minimo <= medido)

# A mesma armadilha do 0.1 + 0.2 do módulo 01:
print(0.1 + 0.2 == 0.3, round(0.1 + 0.2, 4) == 0.3)
