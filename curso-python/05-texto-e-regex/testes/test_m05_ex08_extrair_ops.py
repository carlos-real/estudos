import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_extrair_ops")


def test_acha_varias_ops_na_ordem():
    texto = "Liberar OP 123456 e op-123457. Depois a OP: 123458."
    assert ex.extrair_ops(texto) == ["123456", "123457", "123458"]


def test_nao_repete():
    texto = "OP 123456, OP 654321 e de novo OP 123456"
    assert ex.extrair_ops(texto) == ["123456", "654321"], "Cada OP aparece uma vez só."


@pytest.mark.parametrize(
    "texto",
    ["OP123456", "OP: 123456", "OP - 123456", "op 123456", "OP:-  123456", "(OP 123456)"],
)
def test_separadores_aceitos(texto):
    assert ex.extrair_ops(texto) == ["123456"]


@pytest.mark.parametrize(
    "texto",
    [
        "OP 1234567 tem dígito demais",
        "TOP 111111 não é OP",
        "OP 12345 tem dígito de menos",
        "Sem OPs hoje",
        "",
    ],
)
def test_textos_sem_op_valida(texto):
    assert ex.extrair_ops(texto) == []


def test_texto_com_varias_linhas():
    texto = "Bom dia!\nOP 111111 | NF 1\nOP 222222 | NF 2\n"
    assert ex.extrair_ops(texto) == ["111111", "222222"]
