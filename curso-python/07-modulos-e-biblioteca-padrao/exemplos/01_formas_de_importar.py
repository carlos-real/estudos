"""As quatro formas de importar, lado a lado.

Rode com:  python exemplos/01_formas_de_importar.py
"""

# 1) import modulo  -> use com o prefixo: math.sqrt
import math

# 2) import modulo as apelido  -> apelido curto e conhecido
import statistics as st

# 3) from modulo import nome  -> traz só o nome, sem prefixo
from datetime import date, timedelta

# 4) from modulo import nome as apelido  -> renomeia para evitar conflito
from random import Random as GeradorAleatorio

print("Raiz de 2:", round(math.sqrt(2), 4))
print("Média:", st.mean([25.1, 24.9, 25.3]))
print("Daqui a 30 dias de 29/10/2026:", date(2026, 10, 29) + timedelta(days=30))
gerador = GeradorAleatorio(42)
print("Dado com semente 42:", gerador.randint(1, 6))

# Um módulo importado é um objeto como outro qualquer
print(type(math))
print("De onde veio o statistics?", st.__name__)
