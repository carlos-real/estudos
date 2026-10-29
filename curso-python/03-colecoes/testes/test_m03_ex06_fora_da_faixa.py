import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_fora_da_faixa")


def test_aponta_posicao_e_valor_dos_pontos_fora():
    resultado = ex.fora_da_faixa([50.2, 44.1, 51.0, 56.3], 45.0, 55.0)
    assert resultado == [(2, 44.1), (4, 56.3)], "Posições começam em 1, não em 0."


def test_limites_contam_como_dentro():
    assert ex.fora_da_faixa([45.0, 55.0, 50.0], 45.0, 55.0) == []


def test_todos_fora():
    assert ex.fora_da_faixa([10.0, 99.0], 45.0, 55.0) == [(1, 10.0), (2, 99.0)]


def test_lista_vazia_nao_tem_pontos_fora():
    assert ex.fora_da_faixa([], 45.0, 55.0) == []


def test_resultado_e_lista_de_tuplas():
    resultado = ex.fora_da_faixa([60.0], 45.0, 55.0)
    assert isinstance(resultado, list)
    assert isinstance(resultado[0], tuple), "Cada item deve ser uma tupla (posição, valor)."


@pytest.mark.parametrize(
    ("medicoes", "esperado"),
    [
        ([50.2, 44.1, 51.0, 56.3], 50.0),
        ([50.0, 50.1, 44.0], 66.7),
        ([50.0, 45.0, 55.0], 100.0),
        ([1.0, 2.0], 0.0),
    ],
)
def test_percentual_conforme(medicoes, esperado):
    assert ex.percentual_conforme(medicoes, 45.0, 55.0) == pytest.approx(esperado)


def test_percentual_de_lista_vazia_e_zero():
    assert ex.percentual_conforme([], 45.0, 55.0) == 0.0
