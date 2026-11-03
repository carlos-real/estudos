"""math (contas) e random (sorteios) com exemplos do dia a dia.

Rode com:  python exemplos/09_math_random.py
"""

import math
import random

# Comprimento aproximado do filme numa bobina
diametro_externo = 0.600  # m
diametro_tubete = 0.152  # m (tubete de 6")
espessura = 25e-6  # m (25 µm)
comprimento = math.pi * (diametro_externo**2 - diametro_tubete**2) / (4 * espessura)
print(f"Comprimento da bobina: {comprimento:,.0f} m".replace(",", "."))
print("Bobinas para 50.000 m:", math.ceil(50_000 / comprimento))

# Comparar floats com tolerância
print(0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3))

# random com semente: o mesmo sorteio toda vez (bom para testes e auditoria)
bobinas = [f"B{n:02d}" for n in range(1, 21)]
gerador = random.Random(2026)
print("Sorteio para auditoria:", gerador.sample(bobinas, 3))
print("Um dado:", gerador.randint(1, 6))
print("Uma bobina:", gerador.choice(bobinas))
print("Com reposição:", gerador.choices(["A", "B", "C", "D"], k=5))
