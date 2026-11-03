"""
Solução — Exercício 03.06 — Medições fora da faixa

Ideia central: enumerate dá a posição junto com o valor; compreensões montam a
lista filtrada numa linha legível.
"""


def fora_da_faixa(
    medicoes: list[float], minimo: float, maximo: float
) -> list[tuple[int, float]]:
    """Devolve (posição a partir de 1, valor) de cada medição fora da faixa."""
    # Leia em voz alta: "para cada posição e valor (contando de 1), guarde a
    # tupla (posição, valor) SE o valor NÃO estiver entre mínimo e máximo".
    return [
        (posicao, valor)
        for posicao, valor in enumerate(medicoes, start=1)
        if not minimo <= valor <= maximo
    ]

    # Versão com laço comum (mesmo resultado):
    #     fora = []
    #     for posicao, valor in enumerate(medicoes, start=1):
    #         if valor < minimo or valor > maximo:
    #             fora.append((posicao, valor))
    #     return fora


def percentual_conforme(medicoes: list[float], minimo: float, maximo: float) -> float:
    """Devolve o percentual (0 a 100, 1 casa) de medições dentro da faixa."""
    if not medicoes:  # evita divisão por zero
        return 0.0
    # sum() de booleanos conta os True (True vale 1, False vale 0).
    dentro = sum(minimo <= valor <= maximo for valor in medicoes)
    return round(100 * dentro / len(medicoes), 1)

    # Outra forma, reaproveitando a primeira função:
    #     fora = len(fora_da_faixa(medicoes, minimo, maximo))
    #     return round(100 * (len(medicoes) - fora) / len(medicoes), 1)
