"""
Solução — Exercício 04.06 — CONT.SE e SOMASE em Python

Ideia central: em Python, funções são valores. Dá para passá-las como argumento
(cont_se recebe "condicao") e devolvê-las como resultado (a fábrica).
"""

from collections.abc import Callable


def cont_se(valores: list[float], condicao: Callable[[float], bool]) -> int:
    """Conta os valores que satisfazem a condição."""
    # cont_se não sabe QUAL é o critério; só sabe que pode chamá-lo.
    # sum de booleanos conta os True (módulo 03).
    return sum(1 for valor in valores if condicao(valor))


def soma_se(valores: list[float], condicao: Callable[[float], bool]) -> float:
    """Soma (2 casas) os valores que satisfazem a condição."""
    # sum de uma sequência vazia é 0; float() garante 0.0.
    return round(float(sum(valor for valor in valores if condicao(valor))), 2)


def criar_verificador_faixa(minimo: float, maximo: float) -> Callable[[float], bool]:
    """Fabrica uma função que diz se um valor está na faixa [minimo, maximo]."""

    # A função de dentro "lembra" minimo e maximo mesmo depois que
    # criar_verificador_faixa terminou. Isso se chama closure (fechamento).
    def verificar(valor: float) -> bool:
        return minimo <= valor <= maximo

    return verificar  # SEM parênteses: devolvemos a função, não o resultado dela

    # Versão curta com lambda (equivalente):
    #     return lambda valor: minimo <= valor <= maximo
