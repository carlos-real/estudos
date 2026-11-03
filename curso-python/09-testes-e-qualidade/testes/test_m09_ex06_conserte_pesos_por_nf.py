import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_conserte_pesos_por_nf")


def test_nf_repetida_soma_os_pesos():
    pedidos = [{"nf": "1001", "peso": 250.0}, {"nf": "1001", "peso": 120.5}]
    resultado = ex.somar_pesos_por_nf(pedidos)
    assert resultado == pytest.approx({"1001": 370.5}), (
        "a NF 1001 saiu em dois carregamentos: 250.0 + 120.5 = 370.5"
    )


def test_varias_nfs_misturadas():
    pedidos = [
        {"nf": "1001", "peso": 250.0},
        {"nf": "1002", "peso": 80.0},
        {"nf": "1001", "peso": 120.5},
        {"nf": "1003", "peso": 1000.0},
        {"nf": "1002", "peso": 19.9},
    ]
    resultado = ex.somar_pesos_por_nf(pedidos)
    assert resultado == pytest.approx({"1001": 370.5, "1002": 99.9, "1003": 1000.0})


def test_nf_com_espacos_e_a_mesma_nf():
    pedidos = [
        {"nf": " 1001", "peso": 100.0},
        {"nf": "1001 ", "peso": 50.0},
        {"nf": "1001", "peso": 25.0},
    ]
    resultado = ex.somar_pesos_por_nf(pedidos)
    assert resultado == pytest.approx({"1001": 175.0}), (
        "' 1001', '1001 ' e '1001' são a mesma NF (use strip)"
    )


def test_tres_carregamentos_da_mesma_nf():
    pedidos = [{"nf": "4512", "peso": peso} for peso in (98.7, 120.0, 250.5)]
    assert ex.somar_pesos_por_nf(pedidos) == pytest.approx({"4512": 469.2})
