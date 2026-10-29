"""Exemplo 05 — for sobre strings e range.

Rode com:  python exemplos/05_for_range.py
"""

# for sobre uma string: uma volta por caractere
for letra in "COF":
    print("Letra:", letra)

# range(n): 0, 1, ..., n-1
for i in range(3):
    print("Volta", i)

# range(início, fim): o fim NÃO entra
for bobina in range(1, 4):
    print(f"Bobina {bobina} de 3")

# range(início, fim, passo)
print("De 10 em 10 µm:", end=" ")
for espessura in range(20, 61, 10):
    print(espessura, end=" ")
print()

print("Contagem regressiva:", end=" ")
for n in range(5, 0, -1):
    print(n, end=" ")
print()

# for sobre uma lista recebida (listas a fundo no módulo 03)
pesos = [125.5, 130.2, 128.9]
total = 0.0
for peso in pesos:
    total += peso
print(f"{len(pesos)} bobinas, total {total:.1f} kg")
