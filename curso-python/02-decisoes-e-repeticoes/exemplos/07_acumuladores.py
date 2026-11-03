"""Exemplo 07 — contadores, acumuladores, máximo e mínimo.

Rode com:  python exemplos/07_acumuladores.py
"""

medicoes = [24.8, 25.3, 25.1, 22.7, 25.4, 27.6]
minimo = 23.0
maximo = 27.0

soma = 0.0  # acumulador
quantidade = 0  # contador
fora = 0  # contador com condição
menor = None  # "ainda não vi nenhum valor"
maior = None

for valor in medicoes:
    soma += valor
    quantidade += 1
    if valor < minimo or valor > maximo:
        fora += 1
    if menor is None or valor < menor:
        menor = valor
    if maior is None or valor > maior:
        maior = valor

media = soma / quantidade
print(f"Medições: {quantidade}")
print(f"Média: {media:.2f} µm")
print(f"Menor: {menor} | Maior: {maior} | Amplitude: {maior - menor:.2f}")
print(f"Fora da faixa: {fora} ({fora / quantidade:.0%})")
