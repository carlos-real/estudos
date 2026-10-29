"""Exemplo 04 — while: repetir enquanto a condição for verdadeira.

Rode com:  python exemplos/04_while.py
"""

# 1) Contagem simples
contador = 3
while contador > 0:
    print("Faltam", contador)
    contador -= 1  # sem esta linha, loop infinito!
print("Partiu!")

# 2) Quantos anos para dobrar um capital a 10% ao ano?
capital = 1000.0
anos = 0
while capital < 2000:
    capital *= 1.10
    anos += 1
print(f"Dobrou em {anos} anos: R$ {capital:.2f}")

# 3) O computador adivinha um número de 1 a 100 (busca binária)
secreto = 37
menor = 1
maior = 100
tentativas = 0
while True:
    palpite = (menor + maior) // 2
    tentativas += 1
    print(f"Tentativa {tentativas}: {palpite}")
    if palpite == secreto:
        break
    elif palpite < secreto:
        menor = palpite + 1
    else:
        maior = palpite - 1
print(f"Acertei {secreto} em {tentativas} tentativas.")
