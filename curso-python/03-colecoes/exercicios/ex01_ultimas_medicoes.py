"""
Exercício 03.01 — Últimas medições
Nível: ★☆☆

Contexto: O painel do laboratório mostra só as últimas medições de espessura de
cada linha. Você recebe a lista completa, da mais antiga para a mais recente.

Tarefa: implemente `ultimas_medicoes(medicoes, n)`, que devolve uma lista NOVA
com as `n` últimas medições, na ordem original.
- Se `n` for 0 ou negativo, devolva uma lista vazia.
- Se `n` for maior que o tamanho da lista, devolva todas as medições.
- Não modifique a lista recebida.

Exemplos:
    >>> ultimas_medicoes([50.2, 49.8, 51.0, 50.5], 2)
    [51.0, 50.5]
    >>> ultimas_medicoes([50.2, 49.8], 5)
    [50.2, 49.8]
    >>> ultimas_medicoes([50.2, 49.8], 0)
    []

Dica: fatiamento com índice negativo resolve quase tudo. Mas teste no REPL o que
`[1, 2, 3][-0:]` devolve antes de confiar nele.

Teste com:  python curso.py testar 03 ex01
"""


def ultimas_medicoes(medicoes: list[float], n: int) -> list[float]:
    """Devolve uma lista nova com as n últimas medições, na ordem original."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
