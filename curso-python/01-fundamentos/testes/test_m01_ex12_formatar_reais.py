import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_formatar_reais")


def test_milhar_com_centavos():
    resultado = ex.formatar_reais(1234.56)
    assert resultado == "R$ 1.234,56", f"Sua função devolveu {resultado!r}."


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0, "R$ 0,00"),
        (0.5, "R$ 0,50"),
        (12.3, "R$ 12,30"),
        (1000, "R$ 1.000,00"),
        (1234567.891, "R$ 1.234.567,89"),
        (999999.999, "R$ 1.000.000,00"),
    ],
)
def test_varios_valores(valor, esperado):
    resultado = ex.formatar_reais(valor)
    assert resultado == esperado, f"formatar_reais({valor}) devolveu {resultado!r}."


def test_nao_fica_tudo_com_virgula():
    resultado = ex.formatar_reais(1234.5)
    assert resultado.count(",") == 1, (
        f"Deu {resultado!r}. Use um caractere provisório ao trocar os separadores."
    )
