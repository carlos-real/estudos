from _curso import carregar

ex = carregar(__file__, "ex10_conferir_ops")


def test_cruza_as_tres_listas():
    resultado = ex.conferir_ops(["OP-3", "OP-1", "OP-2"], ["OP-2", "OP-4", "OP-1"])
    assert resultado == {
        "prontas": ["OP-1", "OP-2"],
        "sem_resultado": ["OP-3"],
        "nao_pedidas": ["OP-4"],
    }


def test_remove_repetidos():
    resultado = ex.conferir_ops(["OP-1", "OP-1", "OP-2"], ["OP-1", "OP-1"])
    assert resultado["prontas"] == ["OP-1"], "Cada OP deve aparecer uma vez só."
    assert resultado["sem_resultado"] == ["OP-2"]


def test_listas_em_ordem_alfabetica():
    resultado = ex.conferir_ops(["OP-9", "OP-5", "OP-7"], [])
    assert resultado["sem_resultado"] == ["OP-5", "OP-7", "OP-9"]


def test_tudo_pronto():
    resultado = ex.conferir_ops(["OP-1", "OP-2"], ["OP-2", "OP-1"])
    assert resultado == {"prontas": ["OP-1", "OP-2"], "sem_resultado": [], "nao_pedidas": []}


def test_nenhuma_op_pedida():
    resultado = ex.conferir_ops([], ["OP-1"])
    assert resultado == {"prontas": [], "sem_resultado": [], "nao_pedidas": ["OP-1"]}


def test_valores_sao_listas_e_nao_conjuntos():
    resultado = ex.conferir_ops(["OP-1"], ["OP-1"])
    assert all(isinstance(valor, list) for valor in resultado.values()), (
        "Devolva listas (use sorted), não conjuntos."
    )
