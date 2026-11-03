import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_amplitude")


def test_maior_e_menor_de_uma_serie():
    valores = [24.8, 25.3, 25.1]
    assert ex.maior_valor(valores) == pytest.approx(25.3)
    assert ex.menor_valor(valores) == pytest.approx(24.8)


def test_funciona_com_negativos():
    valores = [-3, -1, -7]
    maior = ex.maior_valor(valores)
    assert maior == -1, (
        f"maior_valor([-3, -1, -7]) devolveu {maior!r}. Você começou com maior = 0? Use None."
    )
    assert ex.menor_valor(valores) == -7


def test_maior_no_comeco_e_menor_no_fim():
    valores = [99.0, 50.0, 10.0]
    assert ex.maior_valor(valores) == pytest.approx(99.0)
    assert ex.menor_valor(valores) == pytest.approx(10.0)


def test_lista_vazia_devolve_none():
    assert ex.maior_valor([]) is None
    assert ex.menor_valor([]) is None


@pytest.mark.parametrize(
    ("valores", "esperado"),
    [
        ([24.8, 25.3, 25.1], 0.5),
        ([-3, -1, -7], 6.0),
        ([5.0], 0.0),
        ([], 0.0),
        ([22.15, 27.9, 25.0, 23.4], 5.75),
    ],
)
def test_amplitude(valores, esperado):
    resultado = ex.amplitude(valores)
    assert resultado == pytest.approx(esperado, abs=1e-9), (
        f"amplitude({valores}) devolveu {resultado!r}; esperado {esperado}."
    )
