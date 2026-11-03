import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_corrigir_lote")


def test_previsao_da_versao_com_defeito():
    assert ex.previsao_bobinas_do_lote_b() == 2, (
        "Rode o código do colega e veja: a lista era compartilhada."
    )


def test_cada_lote_tem_sua_lista():
    a = ex.Lote("L01")
    b = ex.Lote("L02")
    a.adicionar(100.0)
    a.adicionar(120.5)
    b.adicionar(50.0)
    assert a.bobinas == [100.0, 120.5]
    assert b.bobinas == [50.0]
    assert a.peso_total == pytest.approx(220.5)
    assert b.peso_total == pytest.approx(50.0)


def test_lote_novo_comeca_vazio():
    ex.Lote("L01").adicionar(999.0)
    assert ex.Lote("L02").peso_total == 0
    assert ex.Lote("L03").bobinas == []


def test_lote_exportacao_chama_a_mae():
    lote = ex.LoteExportacao("E01", "Chile")
    assert isinstance(lote, ex.Lote)
    assert lote.codigo == "E01"
    assert lote.pais == "Chile"
    lote.adicionar(80.0)
    assert lote.peso_total == pytest.approx(80.0)
    assert ex.Lote("L09").bobinas == []


def test_igualdade_pelo_codigo():
    assert ex.Lote("L01") == ex.Lote("L01")
    assert ex.Lote("L01") != ex.Lote("L02")
    assert ex.LoteExportacao("L01", "Peru") == ex.Lote("L01")


def test_comparar_com_outro_tipo_nao_quebra():
    assert (ex.Lote("L01") == "L01") is False
    assert (ex.Lote("L01") != 1) is True


def test_lote_pode_ir_para_set_e_dict():
    lotes = {ex.Lote("L01"), ex.Lote("L01"), ex.Lote("L02")}
    assert len(lotes) == 2
    pesos = {ex.Lote("L01"): 220.5}
    assert pesos[ex.Lote("L01")] == 220.5
