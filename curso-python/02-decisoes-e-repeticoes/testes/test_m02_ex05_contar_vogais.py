import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_contar_vogais")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("Python", 1),
        ("AEIOU", 5),
        ("aeiou", 5),
        ("bcdfg", 0),
        ("Coeficiente de atrito", 10),
    ],
)
def test_conta_vogais_sem_acento(texto, esperado):
    resultado = ex.contar_vogais(texto)
    assert resultado == esperado, f"contar_vogais({texto!r}) devolveu {resultado}."


@pytest.mark.parametrize(("texto", "esperado"), [("Seleção", 4), ("Ensaio de tração", 8)])
def test_conta_vogais_acentuadas(texto, esperado):
    assert ex.contar_vogais(texto) == esperado


def test_texto_vazio_tem_zero_vogais():
    assert ex.contar_vogais("") == 0
