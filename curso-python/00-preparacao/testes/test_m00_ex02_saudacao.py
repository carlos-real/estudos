import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_saudacao")


@pytest.mark.parametrize(
    ("nome", "esperado"),
    [
        ("Carlos", "Olá, Carlos!"),
        ("Ana", "Olá, Ana!"),
        ("Maria Clara", "Olá, Maria Clara!"),
        ("Laboratório", "Olá, Laboratório!"),
    ],
)
def test_saudacao_com_varios_nomes(nome, esperado):
    assert ex.saudar(nome) == esperado


def test_devolve_um_texto():
    resultado = ex.saudar("Carlos")
    assert resultado is not None, "A função devolveu None. Faltou o return?"
    assert isinstance(resultado, str)


def test_usa_o_nome_recebido_e_nao_um_nome_fixo():
    primeira = ex.saudar("Bruno")
    segunda = ex.saudar("Júlia")
    assert "Bruno" in primeira and "Júlia" in segunda, (
        "A saudação precisa usar o nome que a função recebeu (o parâmetro `nome`)."
    )


def test_nao_muda_maiusculas_do_nome():
    assert ex.saudar("ANA PAULA") == "Olá, ANA PAULA!"
