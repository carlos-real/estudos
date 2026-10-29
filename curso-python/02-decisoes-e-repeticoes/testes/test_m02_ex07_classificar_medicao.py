import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_classificar_medicao")


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (25.4, "DENTRO"),
        (22.5, "DENTRO"),
        (27.5, "DENTRO"),
        (22.49, "ABAIXO"),
        (20.0, "ABAIXO"),
        (27.51, "ACIMA"),
        (31.0, "ACIMA"),
    ],
)
def test_classifica_espessura_25_mais_menos_10(valor, esperado):
    resultado = ex.classificar_medicao(valor, 25, 10)
    assert resultado == esperado, (
        f"classificar_medicao({valor}, 25, 10) devolveu {resultado!r}. Faixa: 22.5 a 27.5."
    )


@pytest.mark.parametrize("valor", [0, -1.5])
def test_valor_zero_ou_negativo_e_invalido(valor):
    assert ex.classificar_medicao(valor, 25, 10) == "INVÁLIDA"


@pytest.mark.parametrize(
    ("valor", "nominal", "tolerancia", "esperado"),
    [
        (52.0, 50, 5, "DENTRO"),
        (47.4, 50, 5, "ABAIXO"),
        (50.0, 50, 0, "DENTRO"),
        (50.1, 50, 0, "ACIMA"),
    ],
)
def test_outras_especificacoes(valor, nominal, tolerancia, esperado):
    assert ex.classificar_medicao(valor, nominal, tolerancia) == esperado
