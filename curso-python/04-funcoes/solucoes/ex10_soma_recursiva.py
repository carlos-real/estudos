"""
Solução — Exercício 04.10 — Recursão: pesos aninhados

Ideia central: uma lista aninhada é "uma lista de coisas que são números OU
listas aninhadas". A função espelha essa definição: número -> caso base;
lista -> chama a si mesma para resolver o pedaço menor.
"""


def soma_aninhada(itens: list) -> float:
    """Soma todos os números de uma lista que pode conter listas em qualquer nível."""
    total = 0
    for item in itens:
        if isinstance(item, list):
            total += soma_aninhada(item)  # caso recursivo: um pedaço MENOR
        else:
            total += item  # caso base: um número
    return total
    # Por que termina? Cada chamada recebe uma lista que está DENTRO da
    # anterior. Uma hora chegamos a listas só com números (ou vazias), e aí
    # o for acaba sem chamar ninguém.


def contar_valores(itens: list) -> int:
    """Conta os números de uma lista que pode conter listas em qualquer nível."""
    # Mesma estrutura, trocando "somar o número" por "contar 1".
    # Versão com expressão geradora: para cada item, ou conta a sublista
    # inteira (recursão) ou conta 1.
    return sum(contar_valores(item) if isinstance(item, list) else 1 for item in itens)
