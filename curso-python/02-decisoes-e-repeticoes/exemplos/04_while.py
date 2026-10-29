"""Exemplo 04 — while: repetir enquanto a condição for verdadeira.

Rode com:  python exemplos/04_while.py
"""

# 1) Contagem simples
contador = 3
while contador > 0:
    print("Faltam", contador)
    contador -= 1  # sem esta linha, loop infinito!
print("Partiu!")

# 2) Em quantos dias o estoque de resina fica abaixo do estoque de segurança?
estoque_kg = 5000.0
consumo_diario_kg = 380.0
estoque_seguranca_kg = 1000.0
dias = 0
while estoque_kg >= estoque_seguranca_kg:
    estoque_kg -= consumo_diario_kg
    dias += 1
print(f"Em {dias} dias o estoque cai para {estoque_kg:.0f} kg: hora de comprar.")

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
