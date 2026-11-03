"""
Exercício 02.09 — Maior, menor e amplitude
Nível: ★★☆

Contexto: A amplitude (maior valor menos o menor) mostra a uniformidade da bobina: uma
espessura média perfeita com amplitude alta indica filme irregular, com pontos finos
que podem rasgar na máquina de envase do cliente.

Tarefa (SEM usar as funções prontas max() e min(): o objetivo é praticar o padrão):
1. `maior_valor(valores)` devolve o maior valor da lista, ou None se estiver vazia.
2. `menor_valor(valores)` devolve o menor valor da lista, ou None se estiver vazia.
3. `amplitude(valores)` devolve maior - menor, arredondado para 2 casas. Para lista
   vazia, devolva 0.0.

Exemplos:
    >>> maior_valor([24.8, 25.3, 25.1])
    25.3
    >>> menor_valor([24.8, 25.3, 25.1])
    24.8
    >>> amplitude([24.8, 25.3, 25.1])
    0.5

Dica: comece com `maior = None`. No laço, se maior ainda é None OU o valor é maior que
ele, atualize. Começar com maior = 0 parece funcionar, mas falha com números
negativos. Teste com [-3, -1, -7].

Teste com:  python curso.py testar 02 ex09
"""


def maior_valor(valores: list[float]) -> float | None:
    """Devolve o maior valor da lista, ou None se ela estiver vazia."""
    # None = "ainda não vi nenhum valor". Para lista vazia, o laço não roda e
    # devolvemos None, exatamente o pedido.
    maior = None
    for valor in valores:
        # "is None" é o jeito certo de perguntar se algo é None. O or tem curto-circuito:
        # na 1ª volta, maior is None é True e o Python nem avalia valor > maior
        # (que daria TypeError comparando float com None).
        if maior is None or valor > maior:
            maior = valor
    return maior


def menor_valor(valores: list[float]) -> float | None:
    """Devolve o menor valor da lista, ou None se ela estiver vazia."""
    menor = None
    for valor in valores:
        if menor is None or valor < menor:
            menor = valor
    return menor


def amplitude(valores: list[float]) -> float:
    """Devolve maior - menor (2 casas), ou 0.0 para lista vazia."""
    maior = maior_valor(valores)
    menor = menor_valor(valores)
    if maior is None or menor is None:
        return 0.0
    # 25.3 - 24.8 dá 0.5000000000000036 por causa do float; o round resolve.
    return round(maior - menor, 2)

    # No módulo 03 você vai usar max(valores) e min(valores), que fazem o mesmo laço
    # por dentro. Saber escrever o padrão à mão é o que permite adaptá-lo (ex.: achar
    # a POSIÇÃO do maior, ou o maior só entre os válidos).
