import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_conceito_nota")


@pytest.mark.parametrize(
    ("nota", "esperado"),
    [
        (10, "A"),
        (9, "A"),
        (8.99, "B"),
        (7, "B"),
        (6.5, "C"),
        (5, "C"),
        (4.99, "D"),
        (0, "D"),
    ],
)
def test_conceito_nas_fronteiras(nota, esperado):
    assert ex.conceito(nota) == esperado


@pytest.mark.parametrize("nota", [-0.1, 10.5, 11, -3])
def test_nota_invalida(nota):
    assert ex.conceito(nota) == "inválida"


@pytest.mark.parametrize(
    ("nota", "frequencia", "esperado"),
    [
        (8.0, 90, "aprovado"),
        (5.0, 75, "aprovado"),
        (4.9, 90, "reprovado por nota"),
        (8.0, 60, "reprovado por falta"),
        (12, 90, "nota inválida"),
    ],
)
def test_situacao(nota, frequencia, esperado):
    assert ex.situacao(nota, frequencia) == esperado


def test_falta_tem_prioridade_sobre_nota_invalida():
    assert ex.situacao(12, 50) == "reprovado por falta", (
        "A frequência é conferida primeiro: falta vence tudo."
    )
