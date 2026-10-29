import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_pesos_por_op")


def test_soma_bobinas_da_mesma_op():
    resultado = ex.pesos_por_op(["OP-4512", "OP-4513", "OP-4512"], [500.0, 320.5, 250.25])
    assert resultado == {"OP-4512": 750.25, "OP-4513": 320.5}


def test_ops_na_ordem_da_primeira_aparicao():
    resultado = ex.pesos_por_op(["OP-9", "OP-1", "OP-9", "OP-5"], [1.0, 2.0, 3.0, 4.0])
    assert list(resultado) == ["OP-9", "OP-1", "OP-5"]


def test_totais_arredondados_em_duas_casas():
    resultado = ex.pesos_por_op(["OP-1", "OP-1", "OP-1"], [0.1, 0.2, 0.3])
    assert resultado["OP-1"] == 0.6, "0.1 + 0.2 + 0.3 dá 0.6000000000000001 sem round(..., 2)."


def test_uma_op_so():
    assert ex.pesos_por_op(["OP-7"], [1250.5]) == {"OP-7": pytest.approx(1250.5)}


@pytest.mark.parametrize(
    ("ops", "pesos"),
    [(["OP-1"], [500.0, 320.5]), (["OP-1", "OP-2"], [500.0]), ([], [10.0])],
)
def test_tamanhos_diferentes_devolvem_dicionario_vazio(ops, pesos):
    assert ex.pesos_por_op(ops, pesos) == {}, "Colunas de tamanhos diferentes: devolva {}."


def test_listas_vazias():
    assert ex.pesos_por_op([], []) == {}
