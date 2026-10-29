"""Exemplo 01 — Listas: criar, acessar e modificar.

Rode na pasta 03-colecoes:  python exemplos/01_listas.py
"""

# Uma lista guarda vários valores, em ordem, numa variável só.
espessuras = [50.2, 49.8, 51.0, 50.5, 48.9]  # µm, bobinas da linha A

print("Medições:", espessuras)
print("Quantidade:", len(espessuras))
print("Primeira:", espessuras[0])
print("Última:", espessuras[-1])

# Trocar um item pelo índice
espessuras[1] = 49.9
print("Corrigi a 2ª:", espessuras)

# Acrescentar no fim
espessuras.append(50.1)
print("append(50.1):", espessuras)

# Inserir numa posição (o resto anda uma casa para a direita)
espessuras.insert(0, 50.0)
print("insert(0, 50.0):", espessuras)

# Remover pelo VALOR (só a primeira ocorrência)
espessuras.remove(48.9)
print("remove(48.9):", espessuras)

# Remover pelo ÍNDICE e receber o valor removido (sem índice: o último)
ultima = espessuras.pop()
print("pop() devolveu", ultima, "e a lista ficou", espessuras)

# Ordenar a PRÓPRIA lista (modifica no lugar e devolve None)
espessuras.sort()
print("sort():", espessuras)

# sorted() devolve uma lista NOVA e não mexe na original
notas = [7.5, 9.0, 6.0]
print("sorted(notas):", sorted(notas), "| notas continua:", notas)

# Perguntas comuns a uma lista
print("50.5 está na lista?", 50.5 in espessuras)
print("Quantas vezes aparece 50.5?", espessuras.count(50.5))
print("Em que posição está 51.0?", espessuras.index(51.0))
