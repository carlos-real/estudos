"""Exemplo 02 — Fatiamento: recortando pedaços de listas (e de strings).

Rode na pasta 03-colecoes:  python exemplos/02_fatiamento.py
"""

medicoes = [50.2, 49.8, 51.0, 50.5, 48.9, 50.1]

print("Do índice 1 ao 3:      ", medicoes[1:4])
print("As 3 primeiras:        ", medicoes[:3])
print("Do índice 3 em diante: ", medicoes[3:])
print("As 2 últimas:          ", medicoes[-2:])
print("Uma sim, uma não:      ", medicoes[::2])
print("Invertida:             ", medicoes[::-1])
print("Cópia inteira:         ", medicoes[:])

# Fatiar nunca dá IndexError: se o fim passa do tamanho, para no fim.
print("Até o índice 100:      ", medicoes[:100])

# Armadilha: -0 é 0. "As últimas 0" vira "do índice 0 em diante" = tudo!
n = 0
print("medicoes[-n:] com n=0: ", medicoes[-n:])

# Strings também fatiam
codigo = "OP-4512-A"
print("Número da OP:", codigo[3:7])
print("Linha:", codigo[-1])
