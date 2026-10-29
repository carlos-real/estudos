import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_soma_recursiva")

CARGA = [[100.0, 120.5], [80.0, [40.0, 40.0]], 10.0]


def test_soma_da_carga():
    assert ex.soma_aninhada(CARGA) == pytest.approx(390.5)


def test_soma_de_lista_sem_aninhamento():
    assert ex.soma_aninhada([1.5, 2.5, 3.0]) == pytest.approx(7.0)


def test_soma_com_muitos_niveis():
    profunda = [1.0, [2.0, [3.0, [4.0, [5.0]]]]]
    assert ex.soma_aninhada(profunda) == pytest.approx(15.0)


@pytest.mark.parametrize("vazia", [[], [[]], [[], [[]]]])
def test_soma_de_listas_vazias_e_zero(vazia):
    assert ex.soma_aninhada(vazia) == 0


def test_contar_valores_da_carga():
    assert ex.contar_valores(CARGA) == 6


def test_contar_com_muitos_niveis():
    assert ex.contar_valores([1.0, [2.0, [3.0, [4.0, [5.0]]]]]) == 5


def test_contar_ignora_as_listas_em_si():
    assert ex.contar_valores([[], [[]], 7.0]) == 1, "Só os números contam, não as listas."


def test_nao_altera_a_carga():
    carga = [[1.0, 2.0], [3.0]]
    ex.soma_aninhada(carga)
    ex.contar_valores(carga)
    assert carga == [[1.0, 2.0], [3.0]]
