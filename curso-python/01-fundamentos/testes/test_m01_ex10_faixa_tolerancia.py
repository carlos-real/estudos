import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_faixa_tolerancia")


@pytest.mark.parametrize(
    ("nominal", "tolerancia", "minimo", "maximo"),
    [
        (25, 10, 22.5, 27.5),
        (50, 5, 47.5, 52.5),
        (40, 7.5, 37.0, 43.0),
        (12, 0, 12.0, 12.0),
    ],
)
def test_limites(nominal, tolerancia, minimo, maximo):
    resultado_min = ex.limite_minimo(nominal, tolerancia)
    resultado_max = ex.limite_maximo(nominal, tolerancia)
    assert resultado_min == pytest.approx(minimo), (
        f"Mínimo de {nominal} ± {tolerancia}% deveria ser {minimo}, deu {resultado_min}."
    )
    assert resultado_max == pytest.approx(maximo), (
        f"Máximo de {nominal} ± {tolerancia}% deveria ser {maximo}, deu {resultado_max}."
    )


def test_descrever_faixa_espessura():
    assert ex.descrever_faixa(25, 10, "µm") == "22.50 a 27.50 µm"


def test_descrever_faixa_gramatura():
    assert ex.descrever_faixa(40, 7.5, "g/m²") == "37.00 a 43.00 g/m²"


def test_descrever_faixa_sem_tolerancia():
    assert ex.descrever_faixa(12, 0, "%") == "12.00 a 12.00 %"
