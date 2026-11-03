"""Exemplo 01 — comparações e operadores lógicos.

Rode com:  python exemplos/01_comparacoes.py
"""

import math

espessura = 25.4
minimo = 23.0
maximo = 27.0

print("Igual a 25.4?", espessura == 25.4)
print("Diferente de 25?", espessura != 25)
print("Maior que o máximo?", espessura > maximo)
print("Menor ou igual ao mínimo?", espessura <= minimo)
print("Dentro da faixa?", minimo <= espessura <= maximo)

# Textos: diferencia maiúsculas e compara caractere a caractere
print("'B' == 'b'?", "B" == "b")
print("'abacaxi' < 'banana'?", "abacaxi" < "banana")
print("'10' < '9'?", "10" < "9")  # texto! compara o '1' com o '9'

# Floats: igualdade exata é perigosa
print("0.1 + 0.2 == 0.3?", 0.1 + 0.2 == 0.3)
print("math.isclose?", math.isclose(0.1 + 0.2, 0.3))

# and, or, not
linha = "C"
liberado = True
print("Linha C e liberado?", linha == "C" and liberado)
print("Linha A ou B?", linha == "A" or linha == "B")
print("Não liberado?", not liberado)
