"""Exemplo 05 — enumerate e zip.

Rode na pasta 03-colecoes:  python exemplos/05_enumerate_zip.py
"""

medicoes = [50.2, 44.1, 51.0]

# enumerate entrega (posição, valor). start=1 conta como gente conta.
for ponto, valor in enumerate(medicoes, start=1):
    print(f"Ponto {ponto}: {valor} µm")

# zip anda por duas (ou mais) listas ao mesmo tempo
ops = ["OP-4512", "OP-4513", "OP-4514"]
pesos = [500.0, 320.5, 210.0]
linhas = ["A", "B", "A"]
for op, peso, linha in zip(ops, pesos, linhas, strict=True):
    print(f"{op} (linha {linha}): {peso} kg")

# zip + dict: duas colunas viram um dicionário
peso_da_op = dict(zip(ops, pesos, strict=True))
print(peso_da_op)

# Sem strict, zip para em silêncio na lista mais curta
curta = ["OP-1", "OP-2"]
print(list(zip(curta, pesos, strict=False)))
