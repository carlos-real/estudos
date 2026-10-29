import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_contem_termo")


def test_encontra_termo_com_caixa_diferente():
    assert ex.contem_termo("COF: liberado", "cof") is True


def test_nao_encontra_termo_ausente():
    assert ex.contem_termo("Tração: OK", "COF") is False


def test_ignora_espacos_nas_pontas_do_termo():
    resultado = ex.contem_termo("cof: LIBERADO", "  liberado ")
    assert resultado is True, "Use strip() no termo antes de procurar."


@pytest.mark.parametrize(
    ("texto", "termo", "esperado"),
    [
        ("Selagem reprovada", "SELAGEM", True),
        ("Liberação parcial", "LIBERAÇÃO", True),
        ("Espessura OK", "gramatura", False),
        ("OP 12345 liberada", "12345", True),
    ],
)
def test_varios_textos(texto, termo, esperado):
    assert ex.contem_termo(texto, termo) is esperado
