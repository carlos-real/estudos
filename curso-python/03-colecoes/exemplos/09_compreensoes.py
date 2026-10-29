"""Exemplo 09 — Compreensões de lista, dicionário e conjunto.

Rode na pasta 03-colecoes:  python exemplos/09_compreensoes.py
"""

espessuras_um = [50.2, 44.1, 51.0, 56.3, 49.8]

# Laço tradicional...
em_mm = []
for valor in espessuras_um:
    em_mm.append(round(valor / 1000, 4))
print("Laço:        ", em_mm)

# ...e a mesma coisa como compreensão
em_mm = [round(valor / 1000, 4) for valor in espessuras_um]
print("Compreensão: ", em_mm)

# Com filtro
fora = [valor for valor in espessuras_um if valor < 45 or valor > 55]
print("Fora de 45-55:", fora)

# Com expressão condicional (transforma todos, sem filtrar)
status = ["ok" if 45 <= valor <= 55 else "fora" for valor in espessuras_um]
print("Status:", status)

# Compreensão de dicionário
ops = ["OP-4512", "OP-4513", "OP-4514"]
pesos = [500.0, 320.5, 210.0]
peso_da_op = {op: peso for op, peso in zip(ops, pesos, strict=True)}
print("Dict:", peso_da_op)
acima_de_300 = {op: peso for op, peso in peso_da_op.items() if peso > 300}
print("Acima de 300 kg:", acima_de_300)

# Compreensão de conjunto
linhas_digitadas = ["a", "A ", " b", "B", "c"]
linhas = {linha.strip().upper() for linha in linhas_digitadas}
print("Linhas distintas:", sorted(linhas))
