"""
Exercício 09.12 — Revisão: escreva os testes de dividir_em_lotes
Nível: ★★★

Solução comentada. Veja o enunciado completo em exercicios/ex12_revisao_testes_lotes.py.
"""

from collections.abc import Callable

import pytest


def testar_dividir_em_lotes(dividir_em_lotes: Callable[[list, int], list[list]]) -> None:
    """Confere a função recebida com asserts. Não devolve nada."""
    # Regra 1: lotes na ordem, último menor (sobra). Pega quem perde a sobra.
    assert dividir_em_lotes(["B1", "B2", "B3", "B4", "B5"], 2) == [
        ["B1", "B2"],
        ["B3", "B4"],
        ["B5"],
    ]

    # Regra 2a: divisão exata, sem lote vazio no final. Pega quem acrescenta []
    # quando a conta "fecha" (um erro clássico de laço com contador).
    assert dividir_em_lotes([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    # Regra 2b: lista vazia devolve lista vazia (e não [[]]).
    assert dividir_em_lotes([], 3) == []

    # Bordas do tamanho: maior que a lista (um lote só) e tamanho 1.
    assert dividir_em_lotes([1, 2], 5) == [[1, 2]]
    assert dividir_em_lotes([1, 2, 3], 1) == [[1], [2], [3]]

    # Regra 3: tamanho inválido. Dois casos: zero e negativo.
    with pytest.raises(ValueError):
        dividir_em_lotes([1, 2, 3], 0)
    with pytest.raises(ValueError):
        dividir_em_lotes([1, 2, 3], -1)

    # Regra 4: não modificar a entrada. Guardamos uma CÓPIA antes (se
    # guardássemos só outra referência, ela mudaria junto; módulo 03) e
    # comparamos depois da chamada.
    bobinas = ["B1", "B2", "B3"]
    copia = bobinas.copy()
    resultado = dividir_em_lotes(bobinas, 2)
    assert resultado == [["B1", "B2"], ["B3"]]
    assert bobinas == copia, "a função não pode alterar a lista recebida"


# Repare na estrutura: cada bloco tem um comentário dizendo QUAL regra protege.
# Quando um teste falhar daqui a 6 meses, quem ler vai entender o porquê.
