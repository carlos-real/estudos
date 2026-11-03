"""
Exercício 04.06 — CONT.SE e SOMASE em Python
Nível: ★★☆

Contexto: No Excel, CONT.SE e SOMASE recebem um intervalo e um CRITÉRIO. Em
Python, o critério pode ser uma FUNÇÃO que você passa como argumento. E uma
função também pode FABRICAR outra função, já configurada.

Tarefa: implemente três funções.
1. `cont_se(valores, condicao)`: quantos valores fazem condicao(valor) ser True.
2. `soma_se(valores, condicao)`: soma dos valores que fazem condicao(valor)
   ser True (0.0 se nenhum), arredondada com round(..., 2).
3. `criar_verificador_faixa(minimo, maximo)`: devolve uma FUNÇÃO que recebe
   um valor e diz (True/False) se ele está entre mínimo e máximo, inclusive.

Exemplos:
    >>> cont_se([50.2, 44.1, 56.3], lambda v: v > 50)
    2
    >>> soma_se([500.0, 320.5, 80.0], lambda p: p >= 100)
    820.5
    >>> dentro = criar_verificador_faixa(45.0, 55.0)
    >>> dentro(50.2), dentro(56.3)
    (True, False)
    >>> cont_se([50.2, 44.1, 56.3], dentro)
    1

Dica: dentro de cont_se, `condicao` é uma variável que guarda uma função; para
usá-la, chame: condicao(valor). Para a fábrica, defina uma função dentro da
outra e devolva-a SEM parênteses (seção 8 da aula).

Teste com:  python curso.py testar 04 ex06
"""

from collections.abc import Callable


def cont_se(valores: list[float], condicao: Callable[[float], bool]) -> int:
    """Conta os valores que satisfazem a condição."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def soma_se(valores: list[float], condicao: Callable[[float], bool]) -> float:
    """Soma (2 casas) os valores que satisfazem a condição."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def criar_verificador_faixa(minimo: float, maximo: float) -> Callable[[float], bool]:
    """Fabrica uma função que diz se um valor está na faixa [minimo, maximo]."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
