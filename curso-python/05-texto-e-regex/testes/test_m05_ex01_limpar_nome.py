import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_limpar_nome")


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("  embalagens   DO sul  ltda ", "Embalagens do Sul Ltda"),
        ("EMBALAGENS DO SUL LTDA", "Embalagens do Sul Ltda"),
        ("plastifort", "Plastifort"),
    ],
)
def test_espacos_e_maiusculas_padronizados(entrada, esperado):
    assert ex.limpar_nome(entrada) == esperado


def test_preposicoes_ficam_minusculas():
    assert ex.limpar_nome("JOÃO DA SILVA E FILHOS DOS SANTOS") == (
        "João da Silva e Filhos dos Santos"
    )


def test_primeira_palavra_sempre_maiuscula():
    assert ex.limpar_nome("de souza plásticos") == "De Souza Plásticos", (
        "Mesmo 'de' ganha maiúscula quando é a primeira palavra."
    )


def test_tabs_e_quebras_de_linha_contam_como_espaco():
    assert ex.limpar_nome("embalagens\tdo\n sul") == "Embalagens do Sul"


@pytest.mark.parametrize("entrada", ["", "   ", "\t\n"])
def test_nome_vazio_devolve_texto_vazio(entrada):
    assert ex.limpar_nome(entrada) == ""
