"""
Exercício 09.03 — Escreva os testes: média das medições
Nível: ★☆☆

Solução comentada. Veja o enunciado completo em exercicios/ex03_testes_media.py.
"""

from collections.abc import Callable

import pytest


def testar_calcular_media(calcular_media: Callable[[list[float]], float]) -> None:
    """Confere a função recebida com asserts. Não devolve nada."""
    # 1) Caso normal com média "quebrada" (não inteira). Pega quem usou //
    #    (divisão inteira) ou arredondou o resultado sem querer.
    assert calcular_media([20.0, 21.0]) == pytest.approx(20.5)
    assert calcular_media([20.1, 19.8, 20.4]) == pytest.approx(20.1)

    # 2) Borda: um valor só. A média é o próprio valor.
    assert calcular_media([7.5]) == pytest.approx(7.5)

    # 3) Negativos: desvios em relação ao nominal. Pega quem usou abs() ou
    #    descartou o sinal. [-1, 1] tem média 0, um caso que denuncia isso.
    assert calcular_media([-2.0, -4.0]) == pytest.approx(-3.0)
    assert calcular_media([-1.0, 1.0]) == pytest.approx(0.0)

    # 4) Erro esperado: lista vazia. Pega quem devolve 0 "para não dar erro".
    with pytest.raises(ValueError):
        calcular_media([])

    # Repare: cada assert existe por um motivo. Antes de escrever um teste,
    # pergunte "que bug este caso pegaria?". Se a resposta for "nenhum novo",
    # talvez ele seja repetido.
