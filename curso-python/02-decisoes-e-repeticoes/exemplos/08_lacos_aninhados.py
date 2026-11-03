"""Exemplo 08 — laços aninhados.

Rode com:  python exemplos/08_lacos_aninhados.py
"""

# Tabuada do 1 ao 3 (laço de fora) até x 4 (laço de dentro)
for n in range(1, 4):
    linha = ""
    for i in range(1, 5):
        linha += f"{n}x{i}={n * i:<4}"
    print(linha)

print()

# Plano de amostragem: cada linha de produção, em cada turno
voltas = 0
for linha_producao in "ABCD":
    for turno in range(1, 4):
        voltas += 1
        print(f"Linha {linha_producao}, turno {turno}", end=" | ")
    print()  # quebra a linha depois dos 3 turnos
print("Total de coletas:", voltas)
