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
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def menor_valor(valores: list[float]) -> float | None:
    """Devolve o menor valor da lista, ou None se ela estiver vazia."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def amplitude(valores: list[float]) -> float:
    """Devolve maior - menor (2 casas), ou 0.0 para lista vazia."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
