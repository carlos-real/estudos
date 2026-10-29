import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_float_para_br")


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (1250.5, "1.250,50"),
        (0.21, "0,21"),
        (980, "980,00"),
        (1234567.891, "1.234.567,89"),
        (0, "0,00"),
    ],
)
def test_duas_casas_por_padrao(valor, esperado):
    assert ex.float_para_br(valor) == esperado


@pytest.mark.parametrize(
    ("valor", "casas", "esperado"),
    [
        (0.215, 3, "0,215"),
        (1250.5, 1, "1.250,5"),
        (25.4, 4, "25,4000"),
    ],
)
def test_quantidade_de_casas_variavel(valor, casas, esperado):
    assert ex.float_para_br(valor, casas) == esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(980, "980"), (12345.678, "12.346"), (1000000, "1.000.000")],
)
def test_zero_casas_sem_virgula(valor, esperado):
    assert ex.float_para_br(valor, 0) == esperado


def test_negativo_mantem_sinal():
    assert ex.float_para_br(-1234567.891, 1) == "-1.234.567,9"
