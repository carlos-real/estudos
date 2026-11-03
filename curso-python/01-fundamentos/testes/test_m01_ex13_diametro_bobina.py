import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_diametro_bobina")


def test_diametro_bobina_tipica():
    resultado = ex.diametro_bobina_mm(4000, 25, 76)
    assert resultado == pytest.approx(364.8, abs=1e-9), (
        f"Esperado 364.8 mm, sua função devolveu {resultado}. "
        "Converteu metros e micrômetros para milímetros antes da fórmula?"
    )


@pytest.mark.parametrize(
    ("comprimento", "espessura", "tubete", "esperado"),
    [
        (0, 25, 76, 76.0),
        (6000, 50, 152, 636.5),
        (12000, 12, 76, 434.9),
        (1000, 20, 76, 176.8),
    ],
)
def test_diametro_varios_casos(comprimento, espessura, tubete, esperado):
    resultado = ex.diametro_bobina_mm(comprimento, espessura, tubete)
    assert resultado == pytest.approx(esperado, abs=1e-9)


@pytest.mark.parametrize(
    ("diametro", "espessura", "tubete", "esperado"),
    [
        (500, 50, 152, 3564),
        (300, 12, 76, 5512),
        (76, 25, 76, 0),
    ],
)
def test_comprimento_varios_casos(diametro, espessura, tubete, esperado):
    resultado = ex.comprimento_bobina_m(diametro, espessura, tubete)
    assert resultado == esperado, f"Esperado {esperado} m, sua função devolveu {resultado}."


def test_comprimento_devolve_inteiro():
    resultado = ex.comprimento_bobina_m(500, 50, 152)
    assert isinstance(resultado, int), "Use round(valor) sem casas: assim ele devolve um int."
