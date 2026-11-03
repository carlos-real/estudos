"""Exemplo 10 — sum, min, max, any, all e sorted com key.

Rode na pasta 03-colecoes:  python exemplos/10_funcoes_embutidas.py
"""

medicoes = [50.2, 49.8, 51.0, 50.5, 48.9]

print("Soma:", round(sum(medicoes), 2))
print("Média:", round(sum(medicoes) / len(medicoes), 2))
print("Menor e maior:", min(medicoes), max(medicoes))

# any: ALGUM satisfaz?  all: TODOS satisfazem?
print("Alguma abaixo de 49?", any(valor < 49 for valor in medicoes))
print("Todas entre 45 e 55?", all(45 <= valor <= 55 for valor in medicoes))

# max/min com lista vazia dão erro; default= evita
print("Máximo de lista vazia:", max([], default=None))

# sorted com key: a key diz O QUE comparar em cada item
bobinas = [
    {"op": "OP-4513", "peso_kg": 320.5},
    {"op": "OP-4512", "peso_kg": 500.0},
    {"op": "OP-4514", "peso_kg": 210.0},
]
por_peso = sorted(bobinas, key=lambda bobina: bobina["peso_kg"])
print("Mais leve primeiro:", [b["op"] for b in por_peso])
mais_pesada = max(bobinas, key=lambda bobina: bobina["peso_kg"])
print("Mais pesada:", mais_pesada["op"])

# Mais perto do nominal: a key é a distância até o nominal
nominal = 49.0
print("Mais perto de 49:", min(medicoes, key=lambda valor: abs(valor - nominal)))

# Vários critérios: tupla na key (nota desc, nome asc)
notas = [("Carla", 8.5), ("Bruno", 9.0), ("Ana", 8.5)]
print(sorted(notas, key=lambda par: (-par[1], par[0])))
