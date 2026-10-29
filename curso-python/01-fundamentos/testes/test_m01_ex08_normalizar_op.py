import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_normalizar_op")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        (" op-12345 ", "OP12345"),
        ("OP 12.345", "OP12345"),
        ("12345", "OP12345"),
        ("Op:  98765", "OP98765"),
        ("OP123456", "OP123456"),
        ("op - 4.321", "OP4321"),
    ],
)
def test_normaliza_varias_formas(texto, esperado):
    resultado = ex.normalizar_op(texto)
    assert resultado == esperado, f"normalizar_op({texto!r}) devolveu {resultado!r}."


def test_ja_normalizada_continua_igual():
    assert ex.normalizar_op("OP55555") == "OP55555"


def test_minusculas_viram_maiusculas_antes_de_remover_op():
    assert ex.normalizar_op("op55555") == "OP55555", (
        "Passe para maiúsculas ANTES de remover 'OP'."
    )
