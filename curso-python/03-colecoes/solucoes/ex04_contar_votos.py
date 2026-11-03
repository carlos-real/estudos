"""
Solução — Exercício 03.04 — Enquete do refeitório

Ideia central: o padrão de CONTAGEM com dicionário. A chave é o que você quer
contar; o valor é quantas vezes apareceu.
"""


def contar_votos(votos: list[str]) -> dict[str, int]:
    """Conta os votos depois de normalizar (strip + lower), ignorando vazios."""
    contagem: dict[str, int] = {}
    for voto in votos:
        prato = voto.strip().lower()
        if not prato:  # string vazia é falsy: pula votos em branco
            continue
        # get(prato, 0): se o prato ainda não apareceu, começa do zero.
        contagem[prato] = contagem.get(prato, 0) + 1
    return contagem

    # No módulo 07 você vai conhecer collections.Counter, que faz isso
    # numa linha. Mas vale saber escrever o padrão na mão.


def vencedor(contagem: dict[str, int]) -> str | None:
    """Devolve o prato mais votado (o primeiro, em caso de empate) ou None."""
    if not contagem:
        return None
    # max percorre as CHAVES do dicionário e compara usando a função key.
    # contagem.get recebe uma chave e devolve o número de votos dela.
    # Em empate, max devolve o primeiro que encontrou (ordem do dicionário).
    return max(contagem, key=contagem.get)

    # Alternativa com laço (módulo 02), também correta:
    #     melhor = None
    #     for prato, votos in contagem.items():
    #         if melhor is None or votos > contagem[melhor]:
    #             melhor = prato
    #     return melhor
