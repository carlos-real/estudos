import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_conserte_numero_br")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("12,5", 12.5),
        ("1.250,50", 1250.5),
        ("0,35", 0.35),
        ("1.000.000,01", 1000000.01),
    ],
)
def test_converte_numeros_com_virgula_decimal(texto, esperado):
    resultado = ex.converter_numero_br(texto)
    assert resultado == pytest.approx(esperado), (
        f"converter_numero_br({texto!r}) devolveu {resultado}, esperado {esperado}"
    )


def test_ignora_espacos_em_volta():
    assert ex.converter_numero_br("  3,75 ") == pytest.approx(3.75)


def test_numero_negativo():
    assert ex.converter_numero_br("-0,5") == pytest.approx(-0.5)


@pytest.mark.parametrize("texto", ["1,2,3", "2,,5"])
def test_texto_com_virgulas_demais_levanta_value_error(texto):
    with pytest.raises(ValueError):
        ex.converter_numero_br(texto)
