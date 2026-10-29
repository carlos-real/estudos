import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_peso_total")


@pytest.mark.parametrize(
    ("peso_bobina_kg", "quantidade", "esperado"),
    [
        (250.0, 4, 1000.0),
        (312.5, 3, 937.5),
        (180.0, 1, 180.0),
        (1250.5, 2, 2501.0),
    ],
)
def test_peso_total_de_varias_cargas(peso_bobina_kg, quantidade, esperado):
    assert ex.peso_total(peso_bobina_kg, quantidade) == pytest.approx(esperado)


def test_quantidade_zero_da_peso_zero():
    assert ex.peso_total(180.0, 0) == 0


def test_multiplica_e_nao_soma():
    resultado = ex.peso_total(5.0, 3)
    assert resultado != 8.0, "Você somou peso e quantidade? O certo é multiplicar."
    assert resultado == pytest.approx(15.0)


def test_numero_quebrado_usa_aproximacao():
    # 12.3 * 3 dá 36.900000000000006 no computador (o módulo 01 explica o porquê).
    # pytest.approx aceita essa diferença minúscula.
    assert ex.peso_total(12.3, 3) == pytest.approx(36.9)
