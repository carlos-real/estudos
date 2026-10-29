import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_media_das_medicoes")


def test_media_de_medicoes_todas_validas():
    resultado = ex.media_valida([24.8, 25.1, 25.3])
    assert resultado == pytest.approx(25.07, abs=1e-9), (
        f"Esperado 25.07, sua função devolveu {resultado!r}. Arredondou com round(..., 2)?"
    )


def test_ignora_zeros_e_negativos():
    resultado = ex.media_valida([25.0, 0, -1, 25.4])
    assert resultado == pytest.approx(25.2, abs=1e-9), (
        f"Esperado 25.2 (média de 25.0 e 25.4), deu {resultado!r}. Pulou os valores <= 0?"
    )


def test_um_valor_so():
    assert ex.media_valida([30.0]) == pytest.approx(30.0)


@pytest.mark.parametrize("valores", [[], [0, 0.0, -2]])
def test_sem_valores_validos_devolve_none(valores):
    resultado = ex.media_valida(valores)
    assert resultado is None, f"media_valida({valores}) deveria ser None, deu {resultado!r}."


@pytest.mark.parametrize(
    ("valores", "esperado"),
    [([25.0, 0, -1, 25.4], 2), ([24.8, 25.1], 0), ([], 0), ([0, 0, 0], 3)],
)
def test_contar_invalidas(valores, esperado):
    assert ex.contar_invalidas(valores) == esperado
