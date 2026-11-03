"""Exemplo 03 — operadores aritméticos, precedência e atribuição composta.

Rode com:  python exemplos/03_operadores.py
"""

print("Soma:", 7 + 2)
print("Subtração:", 7 - 2)
print("Multiplicação:", 7 * 2)
print("Divisão:", 7 / 2)  # / sempre devolve float
print("Divisão inteira:", 7 // 2)  # quantas vezes o 2 cabe inteiro no 7
print("Resto:", 7 % 2)  # o que sobra
print("Potência:", 7**2)

# Precedência: ** primeiro, depois * / // %, por último + -
print("Sem parênteses:", 2 + 3 * 4)
print("Com parênteses:", (2 + 3) * 4)

# Exemplo resolvido: 12.300 m de filme em bobinas de 1.000 m
metros_totais = 12300
metros_por_bobina = 1000
bobinas = metros_totais // metros_por_bobina
sobra = metros_totais % metros_por_bobina
print(bobinas, "bobinas completas e sobra de", sobra, "m")

# Atribuição composta: atualizar a variável usando o valor dela
total_kg = 0
total_kg += 125.5  # o mesmo que total_kg = total_kg + 125.5
total_kg += 130.2
total_kg -= 5.7
print("Peso acumulado:", total_kg)
