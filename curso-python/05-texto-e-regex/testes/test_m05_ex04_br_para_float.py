import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_br_para_float")


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("1.250,50", 1250.5),
        ("25,4", 25.4),
        (" 980 ", 980.0),
        ("0,215", 0.215),
        ("1.000.000,00", 1_000_000.0),
        ("-0,5", -0.5),
    ],
)
def test_converte_formato_brasileiro(entrada, esperado):
    assert ex.br_para_float(entrada) == pytest.approx(esperado)


def test_ponto_sozinho_e_separador_de_milhar():
    assert ex.br_para_float("1.250") == pytest.approx(1250.0), (
        "No Brasil, '1.250' é mil duzentos e cinquenta, e não 1,25."
    )


def test_devolve_float():
    assert isinstance(ex.br_para_float("980"), float)


@pytest.mark.parametrize("entrada", ["abc", "", "25,4 kg"])
def test_texto_invalido_levanta_value_error(entrada):
    with pytest.raises(ValueError):
        ex.br_para_float(entrada)
