import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_resumo_espessura")


def test_resumo_de_quatro_medicoes():
    resumo = ex.resumo_espessura([50.2, 49.8, 51.0, 50.6])
    assert resumo["minimo"] == 49.8
    assert resumo["maximo"] == 51.0
    assert resumo["media"] == pytest.approx(50.4)
    assert resumo["amplitude"] == pytest.approx(1.2)


def test_tem_exatamente_as_quatro_chaves():
    resumo = ex.resumo_espessura([20.0, 21.0])
    assert set(resumo) == {"minimo", "maximo", "media", "amplitude"}, (
        "Use exatamente as chaves minimo, maximo, media e amplitude (sem acento)."
    )


def test_media_e_amplitude_arredondadas_em_duas_casas():
    resumo = ex.resumo_espessura([50.2, 49.8, 51.0, 50.6])
    assert resumo["amplitude"] == 1.2, "A amplitude precisa de round(..., 2)."
    resumo = ex.resumo_espessura([10.0, 10.0, 10.1])
    assert resumo["media"] == 10.03


def test_uma_medicao_so():
    assert ex.resumo_espessura([50.0]) == {
        "minimo": 50.0,
        "maximo": 50.0,
        "media": 50.0,
        "amplitude": 0.0,
    }


def test_lista_vazia_devolve_dicionario_vazio():
    assert ex.resumo_espessura([]) == {}
