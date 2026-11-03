from _curso import carregar

ex = carregar(__file__, "ex01_ultimas_medicoes")


def test_duas_ultimas_medicoes():
    assert ex.ultimas_medicoes([50.2, 49.8, 51.0, 50.5], 2) == [51.0, 50.5]


def test_uma_ultima_medicao_vem_dentro_de_lista():
    assert ex.ultimas_medicoes([50.2, 49.8, 51.0], 1) == [51.0]


def test_n_maior_que_a_lista_devolve_todas():
    assert ex.ultimas_medicoes([50.2, 49.8], 5) == [50.2, 49.8]


def test_n_zero_devolve_lista_vazia():
    resultado = ex.ultimas_medicoes([50.2, 49.8, 51.0], 0)
    assert resultado == [], "Com n = 0 a resposta é []. Lembre que lista[-0:] é a lista toda!"


def test_n_negativo_devolve_lista_vazia():
    assert ex.ultimas_medicoes([50.2, 49.8, 51.0], -2) == []


def test_lista_vazia_devolve_lista_vazia():
    assert ex.ultimas_medicoes([], 3) == []


def test_devolve_lista_nova_sem_mexer_na_original():
    medicoes = [50.2, 49.8, 51.0]
    resultado = ex.ultimas_medicoes(medicoes, 3)
    assert resultado == [50.2, 49.8, 51.0]
    assert resultado is not medicoes, "Devolva uma lista NOVA, não a própria lista recebida."
    resultado.append(99.9)
    assert medicoes == [50.2, 49.8, 51.0]
