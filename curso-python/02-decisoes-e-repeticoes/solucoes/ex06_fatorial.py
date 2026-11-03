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
    if n < 0:
        return None  # retorno antecipado: trata o caso especial e sai
    # Acumulador de MULTIPLICAÇÃO começa em 1 (o "neutro" da multiplicação).
    # Se começasse em 0, tudo vezes 0 daria 0.
    resultado = 1
    # range(2, n + 1) gera 2, 3, ..., n. O fim do range é EXCLUSIVO, daí o + 1.
    # Para n = 0 ou n = 1 o range é vazio, o laço não roda e devolvemos 1. Correto!
    for numero in range(2, n + 1):
        resultado *= numero
    return resultado


def soma_de_1_ate(n: int) -> int:
    """Devolve a soma 1 + 2 + ... + n (0 se n < 1)."""
    # Acumulador de SOMA começa em 0 (o "neutro" da soma).
    total = 0
    # Para n < 1, range(1, n + 1) é vazio e o total fica 0: não precisa de if.
    for numero in range(1, n + 1):
        total += numero
    return total
    # Curiosidade: Gauss calculou isso de cabeça com n * (n + 1) // 2. Laços são
    # ótimos, mas quando existe fórmula, ela é mais rápida.
