"""
Exercício 09.07 — Escreva os testes: classificar uma medição
Nível: ★★☆

Solução comentada. Veja o enunciado completo em exercicios/ex07_testes_classificar.py.
"""

from collections.abc import Callable

import pytest


def testar_classificar(classificar: Callable[[float, float, float], str]) -> None:
    """Confere a função recebida com asserts. Não devolve nada."""
    # Uma "tabela de casos" deixa claro o que está sendo coberto e facilita
    # acrescentar casos novos. É a mesma ideia do @pytest.mark.parametrize.
    casos = [
        # (valor, minimo, maximo, esperado)
        (20.0, 19.0, 21.0, "OK"),  # meio da faixa
        (19.0, 19.0, 21.0, "OK"),  # borda inferior: está DENTRO
        (21.0, 19.0, 21.0, "OK"),  # borda superior: está DENTRO
        (18.9, 19.0, 21.0, "ABAIXO"),  # logo abaixo da borda
        (21.1, 19.0, 21.0, "ACIMA"),  # logo acima da borda
        (5.0, 19.0, 21.0, "ABAIXO"),  # bem abaixo
        (50.0, 19.0, 21.0, "ACIMA"),  # bem acima
        (0.3, 0.3, 0.3, "OK"),  # faixa de um ponto só (mínimo == máximo)
    ]
    for valor, minimo, maximo, esperado in casos:
        obtido = classificar(valor, minimo, maximo)
        # A mensagem diz QUAL caso falhou: sem ela, você só saberia que
        # "algum" caso da lista deu errado.
        assert obtido == esperado, (
            f"classificar({valor}, {minimo}, {maximo}) devolveu {obtido!r}, "
            f"esperado {esperado!r}"
        )

    # Caso de erro: tolerância invertida (mínimo maior que o máximo).
    with pytest.raises(ValueError):
        classificar(20.0, 21.0, 19.0)


# Que bug cada grupo pega:
#   - bordas (19.0 e 21.0 dando "OK"): quem usou < ou > no lugar de <= e >=;
#   - logo abaixo/acima: quem trocou os rótulos ABAIXO e ACIMA;
#   - pytest.raises: quem esqueceu de validar a tolerância.
