import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_dentro_da_faixa")


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (25.4, True),
        (23.0, True),
        (27.0, True),
        (22.99, False),
        (27.01, False),
        (0, False),
    ],
)
def test_dentro_da_faixa(valor, esperado):
    resultado = ex.dentro_da_faixa(valor, 23.0, 27.0)
    assert resultado is esperado, (
        f"dentro_da_faixa({valor}, 23.0, 27.0) devolveu {resultado!r}; esperado {esperado}. "
        "Os limites são inclusivos (<=)."
    )


def test_faixa_de_um_ponto_so():
    assert ex.dentro_da_faixa(5.0, 5.0, 5.0) is True


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(25.0, "OK"), (23.0, "OK"), (27.0, "OK"), (22.9, "FORA"), (30.0, "FORA")],
)
def test_rotular(valor, esperado):
    assert ex.rotular(valor, 23.0, 27.0) == esperado
