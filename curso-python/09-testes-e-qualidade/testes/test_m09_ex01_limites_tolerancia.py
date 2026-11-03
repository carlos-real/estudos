import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_limites_tolerancia")


@pytest.mark.parametrize(
    ("nominal", "tolerancia", "minimo", "maximo"),
    [
        (20.0, 5.0, 19.0, 21.0),  # espessura 20 µm ± 5%
        (25.0, 10.0, 22.5, 27.5),
        (60.0, 2.5, 58.5, 61.5),  # gramatura 60 g/m² ± 2,5%
        (0.3, 20.0, 0.24, 0.36),  # COF 0,30 ± 20%
    ],
)
def test_limites_de_nominal_mais_ou_menos_porcentagem(nominal, tolerancia, minimo, maximo):
    resultado = ex.calcular_limites(nominal, tolerancia)
    assert resultado == pytest.approx((minimo, maximo)), (
        f"para {nominal} ± {tolerancia}% esperava ({minimo}, {maximo})"
    )


def test_devolve_uma_tupla_com_dois_valores():
    resultado = ex.calcular_limites(20.0, 5.0)
    assert isinstance(resultado, tuple), "devolva uma tupla: return minimo, maximo"
    assert len(resultado) == 2


def test_tolerancia_zero_da_minimo_igual_ao_maximo():
    assert ex.calcular_limites(12.0, 0.0) == pytest.approx((12.0, 12.0))


@pytest.mark.parametrize("nominal", [0.0, -5.0])
def test_nominal_zero_ou_negativo_levanta_value_error(nominal):
    with pytest.raises(ValueError):
        ex.calcular_limites(nominal, 5.0)


def test_tolerancia_negativa_levanta_value_error_com_mensagem():
    with pytest.raises(ValueError, match="tolerância"):
        ex.calcular_limites(20.0, -1.0)
