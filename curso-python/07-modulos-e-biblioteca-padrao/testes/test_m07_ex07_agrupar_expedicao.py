from collections import defaultdict

import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_agrupar_expedicao")

EMAIL_1 = [("OP245101", "123456", 1250.5), ("OP245104", "123458", 300.0)]
EMAIL_2 = [("OP245102", "123456", 980.0), ("OP245103", "123457", 410.25)]
EMAIL_3 = [("OP245101", "123456", 200.1)]  # mesma OP e NF de novo (outro volume)
ITENS = EMAIL_1 + EMAIL_2 + EMAIL_3


def test_juntar_emails_mantem_a_ordem():
    assert ex.juntar_emails([EMAIL_1, EMAIL_2, EMAIL_3]) == ITENS


def test_juntar_emails_devolve_lista():
    resultado = ex.juntar_emails([EMAIL_1, EMAIL_2])
    assert isinstance(resultado, list), "Converta o chain em lista com list(...)"
    assert len(resultado) == 4


def test_juntar_emails_com_email_vazio():
    assert ex.juntar_emails([[], EMAIL_2, []]) == EMAIL_2
    assert ex.juntar_emails([]) == []


def test_ops_por_nf_sem_repetir_op():
    assert ex.ops_por_nf(ITENS) == {
        "123456": ["OP245101", "OP245102"],
        "123458": ["OP245104"],
        "123457": ["OP245103"],
    }


def test_ops_por_nf_devolve_dict_comum():
    resultado = ex.ops_por_nf(ITENS)
    assert type(resultado) is dict, "Converta o defaultdict com dict(...) antes de devolver"
    assert list(resultado) == ["123456", "123458", "123457"], "Mantenha a ordem de aparição"


def test_peso_por_nf_soma_volumes():
    assert ex.peso_por_nf(ITENS) == {
        "123456": pytest.approx(2430.6),
        "123458": pytest.approx(300.0),
        "123457": pytest.approx(410.25),
    }


def test_peso_por_nf_arredonda_duas_casas():
    resultado = ex.peso_por_nf([("OP1", "9", 0.1), ("OP2", "9", 0.2)])
    assert resultado == {"9": 0.3}, "0.1 + 0.2 dá 0.30000000000000004: use round(..., 2)"
    assert not isinstance(resultado, defaultdict)


def test_listas_vazias():
    assert ex.ops_por_nf([]) == {}
    assert ex.peso_por_nf([]) == {}
