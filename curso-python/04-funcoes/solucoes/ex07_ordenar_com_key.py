"""
Solução — Exercício 04.07 — Ordenar com key e lambda

Ideia central: a key transforma cada item no "critério de comparação", mas o
resultado continua sendo o item ORIGINAL.
"""


def mais_proxima_do_nominal(medicoes: list[float], nominal: float) -> float | None:
    """Medição mais próxima do nominal (a primeira, em empate) ou None."""
    # A key troca cada medição pela distância até o nominal. O min escolhe a
    # menor distância e devolve a MEDIÇÃO. Em empate, min fica com a primeira.
    # default=None cobre a lista vazia.
    return min(medicoes, key=lambda valor: abs(valor - nominal), default=None)


def ordenar_por_desvio(medicoes: list[float], nominal: float) -> list[float]:
    """Nova lista, da medição mais próxima do nominal para a mais distante."""
    # sorted é ESTÁVEL: itens com a mesma key mantêm a ordem original.
    return sorted(medicoes, key=lambda valor: abs(valor - nominal))


def ordenar_palavras(palavras: list[str]) -> list[str]:
    """Nova lista por tamanho e, no empate, alfabética sem diferenciar maiúsculas."""
    # Tupla na key: compara o tamanho; se empatar, compara a palavra minúscula.
    return sorted(palavras, key=lambda palavra: (len(palavra), palavra.lower()))

    # Com def no lugar da lambda (útil quando a regra cresce):
    #     def criterio(palavra):
    #         return len(palavra), palavra.lower()
    #     return sorted(palavras, key=criterio)
