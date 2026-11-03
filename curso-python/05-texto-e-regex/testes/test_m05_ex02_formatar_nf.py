import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_formatar_nf")


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("12345", "000.012.345"),
        ("123456789", "123.456.789"),
        ("7", "000.000.007"),
    ],
)
def test_completa_com_zeros_e_pontua(entrada, esperado):
    assert ex.formatar_nf(entrada) == esperado


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("NF-e 98.765", "000.098.765"),
        ("  NF 12345 ", "000.012.345"),
        ("000.012.345", "000.012.345"),
    ],
)
def test_ignora_o_que_nao_e_digito(entrada, esperado):
    assert ex.formatar_nf(entrada) == esperado


@pytest.mark.parametrize("entrada", ["", "sem número", "NF-e"])
def test_sem_digitos_devolve_vazio(entrada):
    assert ex.formatar_nf(entrada) == ""
