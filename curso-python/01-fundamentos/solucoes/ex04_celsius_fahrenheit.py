"""
Exercício 01.04 — Celsius e Fahrenheit
Nível: ★☆☆

Contexto: O manual da seladora importada traz as temperaturas em °F, mas o
procedimento do laboratório usa °C. Você vai escrever as duas conversões.

Tarefa:
1. `celsius_para_fahrenheit(celsius)` devolve a temperatura em °F:
   F = C * 9 / 5 + 32
2. `fahrenheit_para_celsius(fahrenheit)` faz o caminho inverso:
   C = (F - 32) * 5 / 9
Não arredonde os resultados.

Exemplos:
    >>> celsius_para_fahrenheit(100)
    212.0
    >>> fahrenheit_para_celsius(32)
    0.0

Dica: na fórmula inversa, os parênteses em (F - 32) são obrigatórios. Por quê?

Teste com:  python curso.py testar 01 ex04
"""


def celsius_para_fahrenheit(celsius: float) -> float:
    """Converte graus Celsius para Fahrenheit."""
    # Multiplicação e divisão acontecem antes da soma, então não há parênteses aqui.
    # O resultado é float mesmo com celsius inteiro, porque / sempre devolve float.
    return celsius * 9 / 5 + 32


def fahrenheit_para_celsius(fahrenheit: float) -> float:
    """Converte graus Fahrenheit para Celsius."""
    # Aqui os parênteses são obrigatórios: primeiro tiramos 32, DEPOIS multiplicamos.
    # Sem eles, o Python calcularia 32 * 5 / 9 e subtrairia de fahrenheit.
    return (fahrenheit - 32) * 5 / 9
