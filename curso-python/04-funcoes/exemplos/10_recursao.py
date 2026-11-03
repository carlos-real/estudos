"""Exemplo 10 — Recursão: uma função que chama a si mesma.

Rode na pasta 04-funcoes:  python exemplos/10_recursao.py
"""


def fatorial(n, nivel=0):
    """n! = n × (n−1)!, com 0! = 1. 'nivel' só serve para indentar o rastro."""
    recuo = "  " * nivel
    print(f"{recuo}fatorial({n}) chamado")
    if n == 0:  # caso base: para de chamar
        print(f"{recuo}fatorial(0) devolve 1")
        return 1
    resultado = n * fatorial(n - 1, nivel + 1)  # caso recursivo: problema menor
    print(f"{recuo}fatorial({n}) devolve {resultado}")
    return resultado


fatorial(3)


def soma_aninhada(itens):
    """Soma números em listas dentro de listas, em qualquer profundidade."""
    total = 0
    for item in itens:
        if isinstance(item, list):
            total += soma_aninhada(item)
        else:
            total += item
    return total


carga = [[100.0, 120.5], [80.0, [40.0, 40.0]], 10.0]
print("Peso total da carga:", soma_aninhada(carga), "kg")


def soma_com_laco(valores):
    """Para listas 'retas', o laço é mais simples e mais rápido que a recursão."""
    total = 0
    for valor in valores:
        total += valor
    return total


print("Soma reta:", soma_com_laco([1, 2, 3]))
