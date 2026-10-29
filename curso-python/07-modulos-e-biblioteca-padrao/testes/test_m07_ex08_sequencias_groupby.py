import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_sequencias_groupby")


@pytest.mark.parametrize(
    ("resultados", "esperado"),
    [
        (["A", "A", "R", "R", "R", "A"], [("A", 2), ("R", 3), ("A", 1)]),
        (["R"], [("R", 1)]),
        (["A", "R", "A", "R"], [("A", 1), ("R", 1), ("A", 1), ("R", 1)]),
        ([], []),
    ],
)
def test_resumir_sequencia(resultados, esperado):
    assert ex.resumir_sequencia(resultados) == esperado


@pytest.mark.parametrize(
    ("resultados", "esperado"),
    [
        (["R", "A", "R", "R", "A"], 2),
        (["A", "A", "A"], 0),
        (["R", "R", "R", "A", "R", "R"], 3),
        ([], 0),
    ],
)
def test_maior_sequencia_de_reprovadas(resultados, esperado):
    assert ex.maior_sequencia(resultados) == esperado


def test_maior_sequencia_com_outro_alvo():
    assert ex.maior_sequencia(["A", "A", "R", "A", "A", "A"], alvo="A") == 3


def test_peso_por_lote_fora_de_ordem():
    bobinas = [("L02", 150.0), ("L01", 120.5), ("L02", 149.5), ("L03", 98.0), ("L01", 121.0)]
    assert ex.peso_por_lote(bobinas) == [("L01", 241.5), ("L02", 299.5), ("L03", 98.0)], (
        "Cada lote deve aparecer uma vez só: ordene antes do groupby."
    )


def test_peso_por_lote_arredonda():
    assert ex.peso_por_lote([("L9", 0.1), ("L9", 0.2)]) == [("L9", 0.3)]


def test_peso_por_lote_vazio():
    assert ex.peso_por_lote([]) == []
