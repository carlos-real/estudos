import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_conferir_linha")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("A", "A"), (" a ", "A"), ("Linha B", "B"), ("LINHA  c", "C"), ("linha d", "D")],
)
def test_normalizar_linha_reconhece(texto, esperado):
    assert ex.normalizar_linha(texto) == esperado


@pytest.mark.parametrize("texto", ["Linha E", "AB", "", "   ", None, "Resumo", "Linha A2"])
def test_normalizar_linha_recusa(texto):
    assert ex.normalizar_linha(texto) is None


@pytest.mark.parametrize("informada", ["B", "b", " Linha B ", "linha b"])
def test_linha_que_bate_com_a_aba(informada):
    assert ex.conferir_linha("Linha B", informada) is None


def test_linha_diferente_da_aba():
    assert ex.conferir_linha("Linha B", "C") == "linha informada C diferente da aba Linha B"
    assert ex.conferir_linha("Linha A", "linha d") == (
        "linha informada D diferente da aba Linha A"
    )


@pytest.mark.parametrize(
    ("informada", "esperado"),
    [
        (None, "linha não informada ou inválida: ''"),
        ("", "linha não informada ou inválida: ''"),
        ("E", "linha não informada ou inválida: 'E'"),
    ],
)
def test_linha_vazia_ou_invalida(informada, esperado):
    assert ex.conferir_linha("Linha A", informada) == esperado


def test_aba_que_nao_e_de_linha():
    esperado = "aba 'Resumo' não corresponde a uma linha de produção"
    assert ex.conferir_linha("Resumo", "A") == esperado
