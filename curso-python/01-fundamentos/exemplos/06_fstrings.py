"""Exemplo 06 — f-strings e formatação de números.

Rode com:  python exemplos/06_fstrings.py
"""

op = "OP12345"
media = 25.0666
peso = 1250.5
aprovadas = 0.956
lote = 7

print(f"OP {op}: média {media} µm")
print(f"Média com 2 casas: {media:.2f}")
print(f"Peso com milhar: {peso:,.2f} kg")
print(f"Aprovação: {aprovadas:.1%}")
print(f"Lote com zeros: {lote:03d}")
print(f"Desvio com sinal: {-0.35:+.2f} | {0.35:+.2f}")
print(f"Conta dentro das chaves: {peso / 8:.1f} kg por bobina")

# Alinhamento: < esquerda, > direita, ^ centro (o número é a largura)
print(f"[{'COF':<10}]")
print(f"[{'COF':>10}]")
print(f"[{'COF':^10}]")
print(f"{'Ensaio':<12}{'Resultado':>10}")
print(f"{'Espessura':<12}{25.07:>10.2f}")
print(f"{'Gramatura':<12}{52.3:>10.2f}")

# Depuração rápida: com = a f-string mostra o nome e o valor
print(f"{media=}")
