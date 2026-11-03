"""Exemplo 06 — break e continue.

Rode com:  python exemplos/06_break_continue.py
"""

medicoes = [25.1, 0.0, 24.8, 31.2, 25.0, -1.0, 26.9]

# continue: pula o resto desta volta e vai para a próxima
print("Medições válidas:", end=" ")
for valor in medicoes:
    if valor <= 0:
        continue
    print(valor, end=" ")
print()

# break: encerra o laço na hora
posicao = 0
for valor in medicoes:
    posicao += 1
    if valor > 27:
        print(f"Primeira acima de 27 µm: {valor} (posição {posicao}). Parando a busca.")
        break

# O laço termina; o programa continua normalmente depois dele
print("Fim da inspeção.")
