import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_validar_op")


@pytest.mark.parametrize(
    "codigo",
    ["OP 123456", "OP-123456", "OP123456", "op 123456", "Op-004512", "  OP 123456  "],
)
def test_codigos_validos(codigo):
    assert ex.validar_op(codigo) is True, f"{codigo!r} deveria ser válido"


@pytest.mark.parametrize(
    "codigo",
    [
        "OP 12345",
        "OP 1234567",
        "OS 123456",
        "XOP 123456",
        "OP  123456",
        "OP - 123456",
        "OP 123456 cancelada",
        "OP 12345a",
        "123456",
        "",
    ],
)
def test_codigos_invalidos(codigo):
    assert ex.validar_op(codigo) is False, f"{codigo!r} NÃO deveria ser válido"


def test_devolve_bool_e_nao_match():
    resultado = ex.validar_op("OP 123456")
    assert type(resultado) is bool, "Devolva True/False, e não o objeto Match."
