import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_media_notas")


def test_media_de_tres_notas_inteiras():
    resultado = ex.calcular_media(7, 8, 9)
    assert resultado == pytest.approx(8.0), (
        f"A média de 7, 8 e 9 é 8.0, mas sua função devolveu {resultado}. "
        "Lembrou dos parênteses em (nota1 + nota2 + nota3) / 3?"
    )


@pytest.mark.parametrize(
    ("n1", "n2", "n3", "esperado"),
    [
        (10, 0, 5, 5.0),
        (6.5, 7.0, 8.25, 7.25),
        (0, 0, 0, 0.0),
        (10, 10, 10, 10.0),
    ],
)
def test_media_de_varios_casos(n1, n2, n3, esperado):
    assert ex.calcular_media(n1, n2, n3) == pytest.approx(esperado)


def test_media_ponderada_prova_com_peso_dois():
    assert ex.calcular_media_ponderada(8, 2, 5, 1) == pytest.approx(7.0)


@pytest.mark.parametrize(
    ("n1", "p1", "n2", "p2", "esperado"),
    [
        (10, 1, 0, 1, 5.0),
        (6, 3, 9, 1, 6.75),
        (7.5, 1, 7.5, 4, 7.5),
    ],
)
def test_media_ponderada_varios_casos(n1, p1, n2, p2, esperado):
    assert ex.calcular_media_ponderada(n1, p1, n2, p2) == pytest.approx(esperado)
