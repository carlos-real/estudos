import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_classe_amostra")


def test_init_guarda_e_normaliza_atributos():
    a = ex.Amostra(" am-001 ", " Espessura ", 25.3, "µm")
    assert a.codigo == "AM-001"
    assert a.ensaio == "espessura"
    assert a.valor == pytest.approx(25.3)
    assert a.unidade == "µm"


def test_valor_vira_float_e_unidade_padrao_vazia():
    a = ex.Amostra("AM-002", "cof", 1)
    assert type(a.valor) is float, "Converta o valor com float(...)"
    assert a.unidade == ""


@pytest.mark.parametrize(
    ("args", "esperado"),
    [
        (("am-001", "espessura", 25.3, "µm"), "AM-001 | espessura = 25.30 µm"),
        (("AM-002", "COF", 0.25), "AM-002 | cof = 0.25"),
        (("am-003", "gramatura", 23, "g/m²"), "AM-003 | gramatura = 23.00 g/m²"),
    ],
)
def test_descricao(args, esperado):
    assert ex.Amostra(*args).descricao() == esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(22.5, True), (27.5, True), (25.0, True), (22.4, False), (28, False)],
)
def test_esta_entre_com_limites_inclusos(valor, esperado):
    assert ex.Amostra("AM-1", "espessura", valor).esta_entre(22.5, 27.5) is esperado


def test_cada_objeto_tem_seus_proprios_dados():
    a = ex.Amostra("AM-1", "espessura", 25.0)
    b = ex.Amostra("AM-2", "cof", 0.2)
    a.valor = 30.0
    assert b.valor == pytest.approx(0.2)
    assert a.descricao() == "AM-1 | espessura = 30.00"
