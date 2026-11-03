"""
Exercício 03.06 — Medições fora da faixa
Nível: ★★☆

Contexto: Ao medir a espessura em vários pontos de uma bobina, o analista precisa
saber QUAIS pontos ficaram fora da faixa (e não só quantos), para anotar no laudo.

Tarefa: implemente duas funções.
1. `fora_da_faixa(medicoes, minimo, maximo)` devolve uma lista de tuplas
   (posição, valor) das medições fora da faixa [minimo, maximo].
   - A posição começa em 1 (é assim que o analista conta os pontos).
   - Os limites contam como dentro da faixa.
2. `percentual_conforme(medicoes, minimo, maximo)` devolve o percentual de
   medições DENTRO da faixa, arredondado com round(..., 1).
   Lista vazia: devolva 0.0.

Exemplos:
    >>> fora_da_faixa([50.2, 44.1, 51.0, 56.3], 45.0, 55.0)
    [(2, 44.1), (4, 56.3)]
    >>> percentual_conforme([50.2, 44.1, 51.0, 56.3], 45.0, 55.0)
    50.0
    >>> percentual_conforme([50.0, 50.1, 44.0], 45.0, 55.0)
    66.7

Dica: enumerate(medicoes, start=1) entrega (posição, valor). Tente escrever a
primeira função com uma compreensão de lista.

Teste com:  python curso.py testar 03 ex06
"""


def fora_da_faixa(
    medicoes: list[float], minimo: float, maximo: float
) -> list[tuple[int, float]]:
    """Devolve (posição a partir de 1, valor) de cada medição fora da faixa."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def percentual_conforme(medicoes: list[float], minimo: float, maximo: float) -> float:
    """Devolve o percentual (0 a 100, 1 casa) de medições dentro da faixa."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
