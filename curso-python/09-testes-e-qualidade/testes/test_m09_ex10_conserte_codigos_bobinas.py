import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_conserte_codigos_bobinas")


def test_tres_bobinas_comecam_em_001():
    assert ex.gerar_codigos_bobinas("12345", 3) == ["12345-001", "12345-002", "12345-003"]


def test_uma_bobina():
    assert ex.gerar_codigos_bobinas("777", 1) == ["777-001"]


def test_muitas_bobinas_terminam_na_quantidade():
    codigos = ex.gerar_codigos_bobinas("98765", 120)
    assert codigos[0] == "98765-001", "a numeração começa em 001"
    assert codigos[-1] == "98765-120", "a última etiqueta tem o número da quantidade"
    assert len(codigos) == 120


def test_op_com_espacos_em_volta():
    assert ex.gerar_codigos_bobinas(" 4512 ", 2) == ["4512-001", "4512-002"]


@pytest.mark.parametrize("quantidade", [0, -3])
def test_quantidade_menor_que_um_levanta_value_error(quantidade):
    with pytest.raises(ValueError):
        ex.gerar_codigos_bobinas("12345", quantidade)
