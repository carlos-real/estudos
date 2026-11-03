import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_celsius_fahrenheit")


@pytest.mark.parametrize(
    ("celsius", "fahrenheit"),
    [(0, 32.0), (100, 212.0), (-40, -40.0), (37, 98.6), (150, 302.0)],
)
def test_celsius_para_fahrenheit(celsius, fahrenheit):
    resultado = ex.celsius_para_fahrenheit(celsius)
    assert resultado == pytest.approx(fahrenheit), (
        f"{celsius} °C deveria dar {fahrenheit} °F, mas deu {resultado}."
    )


@pytest.mark.parametrize(
    ("fahrenheit", "celsius"),
    [(32, 0.0), (212, 100.0), (-40, -40.0), (98.6, 37.0), (302, 150.0)],
)
def test_fahrenheit_para_celsius(fahrenheit, celsius):
    resultado = ex.fahrenheit_para_celsius(fahrenheit)
    assert resultado == pytest.approx(celsius), (
        f"{fahrenheit} °F deveria dar {celsius} °C, mas deu {resultado}. "
        "Confira os parênteses em (F - 32)."
    )


def test_ida_e_volta_devolve_o_valor_original():
    temperatura = 180.0
    volta = ex.fahrenheit_para_celsius(ex.celsius_para_fahrenheit(temperatura))
    assert volta == pytest.approx(temperatura)
