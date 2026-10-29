import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_dividir_lote")


@pytest.mark.parametrize(
    ("total", "bobina", "esperado"),
    [
        (1250.5, 300, (4, 50.5)),
        (900, 300, (3, 0.0)),
        (100, 300, (0, 100.0)),
        (1000.3, 250, (4, 0.3)),
    ],
)
def test_divide_em_bobinas_e_sobra(total, bobina, esperado):
    assert ex.dividir_em_bobinas(total, bobina) == esperado


def test_devolve_tupla_com_inteiro():
    resultado = ex.dividir_em_bobinas(1250.5, 300)
    assert isinstance(resultado, tuple), "Devolva uma tupla: return bobinas, sobra"
    assert isinstance(resultado[0], int), "A quantidade de bobinas deve ser int (use int())."


@pytest.mark.parametrize("bobina", [0, -10])
def test_peso_de_bobina_invalido_devolve_none(bobina):
    assert ex.dividir_em_bobinas(500, bobina) is None


def test_descrever_divisao():
    assert ex.descrever_divisao(1250.5, 300) == "4 bobinas de 300.0 kg + sobra de 50.5 kg"
    assert ex.descrever_divisao(900, 300) == "3 bobinas de 300.0 kg + sobra de 0.0 kg"


def test_descrever_divisao_com_peso_invalido():
    assert ex.descrever_divisao(500, 0) == "peso da bobina inválido"
