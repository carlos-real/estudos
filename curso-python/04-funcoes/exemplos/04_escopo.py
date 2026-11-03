"""Exemplo 04 — Escopo: variáveis locais, globais e objetos recebidos.

Rode na pasta 04-funcoes:  python exemplos/04_escopo.py
"""

TOLERANCIA_PADRAO = 10.0  # global "constante": lida, nunca alterada


def limites(nominal):
    fator = TOLERANCIA_PADRAO / 100  # "fator" é LOCAL; a global só é lida
    return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)


print(limites(50.0))
print("fator existe fora da função?", "fator" in globals())

total = 0


def somar(valor):
    total = valor + 1  # cria uma variável LOCAL chamada total
    return total


print("somar(10) devolveu", somar(10), "| total global continua", total)


def reatribuir(valores):
    valores = [0, 0]  # move só a etiqueta local
    return valores


def modificar(valores):
    valores.append(0)  # mexe no objeto que veio de fora


a = [1, 2]
b = [1, 2]
reatribuir(a)
modificar(b)
print("a:", a, "| b:", b)
