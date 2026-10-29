"""
Exercício 02.06 — Fatorial e soma acumulada
Nível: ★☆☆

Contexto: Dois clássicos para praticar for, range e acumuladores. O fatorial aparece em
combinatória e estatística: de quantas formas dá para ordenar n amostras?

Tarefa:
1. `fatorial(n)` devolve n! = 1 x 2 x 3 x ... x n. Por definição, 0! = 1.
   Se n for negativo, devolva None.
2. `soma_de_1_ate(n)` devolve 1 + 2 + ... + n. Se n for menor que 1, devolva 0.
Use laços for com range (não use fórmulas prontas nem math.factorial).

Exemplos:
    >>> fatorial(5)
    120
    >>> fatorial(0)
    1
    >>> soma_de_1_ate(100)
    5050

Dica: para multiplicar, o acumulador começa em 1 (não em 0!). Por quê?

Teste com:  python curso.py testar 02 ex06
"""


def fatorial(n: int) -> int | None:
    """Devolve n!, ou None se n for negativo."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def soma_de_1_ate(n: int) -> int:
    """Devolve a soma 1 + 2 + ... + n (0 se n < 1)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
