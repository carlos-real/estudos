"""Exemplo 07 — lambda e o parâmetro key=.

Rode na pasta 04-funcoes:  python exemplos/07_lambda_key.py
"""

bobinas = [
    {"op": "OP-4513", "peso_kg": 320.5, "espessura": 50.9},
    {"op": "OP-4512", "peso_kg": 500.0, "espessura": 49.2},
    {"op": "OP-4514", "peso_kg": 210.0, "espessura": 50.1},
]

# key com lambda: "para cada bobina, compare o peso"
for b in sorted(bobinas, key=lambda bobina: bobina["peso_kg"]):
    print(b["op"], b["peso_kg"])

# a mesma key com def (melhor quando a regra tem nome ou cresce)


def desvio_do_nominal(bobina):
    return abs(bobina["espessura"] - 50.0)


mais_proxima = min(bobinas, key=desvio_do_nominal)
print("Mais perto de 50 µm:", mais_proxima["op"])

# vários critérios: espessura decrescente e, no empate, OP crescente
ordenadas = sorted(bobinas, key=lambda b: (-b["espessura"], b["op"]))
print([b["op"] for b in ordenadas])
