"""
Exercício 03.05 — Lotes sem repetição
Nível: ★☆☆

Contexto: O leitor de código de barras da expedição às vezes lê o mesmo lote
duas vezes. Você precisa da lista de lotes sem repetição, mantendo a ordem em
que cada lote foi lido pela primeira vez.

Tarefa: implemente `remover_duplicadas(itens)`, que devolve uma lista NOVA:
- sem itens repetidos;
- na ordem da primeira ocorrência de cada item;
- sem modificar a lista recebida.

Exemplos:
    >>> remover_duplicadas(["L-101", "L-102", "L-101", "L-103", "L-102"])
    ['L-101', 'L-102', 'L-103']
    >>> remover_duplicadas([])
    []

Dica: `list(set(itens))` remove repetidos, mas BAGUNÇA a ordem. Use um conjunto
só para lembrar "o que eu já vi" e uma lista para o resultado.

Teste com:  python curso.py testar 03 ex05
"""


def remover_duplicadas(itens: list[str]) -> list[str]:
    """Devolve uma lista nova, sem repetidos, na ordem da primeira ocorrência."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
