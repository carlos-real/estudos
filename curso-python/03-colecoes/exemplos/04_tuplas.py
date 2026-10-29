"""Exemplo 04 — Tuplas e desempacotamento.

Rode na pasta 03-colecoes:  python exemplos/04_tuplas.py
"""

# Uma tupla é um registro fixo: OP, linha, peso.
bobina = ("OP-4512", "A", 1250.5)
print("Registro:", bobina)
print("Peso:", bobina[2])

# Desempacotar: cada posição vai para uma variável
op, linha, peso = bobina
print(f"{op} | linha {linha} | {peso} kg")

# Trocar valores sem variável auxiliar
minimo, maximo = 55.0, 45.0  # digitados ao contrário
minimo, maximo = maximo, minimo
print("Faixa corrigida:", minimo, "a", maximo)

# Estrela: "o resto vai para cá" (sempre vira lista)
medicoes = [50.2, 49.8, 51.0, 50.5]
primeira, *meio, ultima = medicoes
print("primeira:", primeira, "| meio:", meio, "| última:", ultima)

# Desempacotar dentro do for
pedidos = [("OP-4512", 500.0), ("OP-4513", 320.5)]
for op, peso in pedidos:
    print(f"{op}: {peso} kg")

# Tupla de um item precisa de vírgula
um_item = (50.2,)
nao_e_tupla = 50.2
print(type(um_item), type(nao_e_tupla))
