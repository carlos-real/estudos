import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_ler_numero")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("1.250,5", 1250.5), ("25,4", 25.4), (" 980 ", 980.0), ("-0,5", -0.5)],
)
def test_converte_numeros_validos(texto, esperado):
    assert ex.ler_numero(texto) == pytest.approx(esperado)


@pytest.mark.parametrize("texto", ["#N/D", "", "   ", "25,4 kg", "abc"])
def test_texto_invalido_devolve_none(texto):
    assert ex.ler_numero(texto) is None


def test_texto_invalido_devolve_o_padrao_informado():
    assert ex.ler_numero("#N/D", padrao=0.0) == 0.0
    assert ex.ler_numero("", padrao=-1.0) == -1.0


@pytest.mark.parametrize("texto", ["0", "0,0"])
def test_zero_valido_nao_e_trocado_pelo_padrao(texto):
    assert ex.ler_numero(texto, padrao=-1.0) == 0.0, (
        "Zero é um número válido. Cuidado com 'valor or padrao': 0.0 é falsy."
    )
