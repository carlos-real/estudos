"""Exemplo 05 — conversões entre tipos e input().

Rode com:  python exemplos/05_conversoes_e_input.py

Para não travar esperando digitação, este exemplo SIMULA o que o usuário digitaria.
Para testar de verdade, troque a linha marcada por input().
"""

# texto_peso = input("Peso da bobina (kg): ")  # versão interativa
texto_peso = "125,5"  # simulação: o que a pessoa digitou

print("Tipo do que veio do teclado:", type(texto_peso))
print("Somar textos cola os textos:", "25" + "5")

peso = float(texto_peso.replace(",", "."))  # vírgula -> ponto, depois converte
print("Peso convertido:", peso, type(peso))
print("Dobro do peso:", peso * 2)

print("int('42'):", int("42"))
print("int(25.9) corta as casas:", int(25.9))
print("float('7'):", float("7"))
print("str(12345):", str(12345), type(str(12345)))
print("Juntando com str():", "OP" + str(12345))
