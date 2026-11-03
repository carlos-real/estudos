import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_leitura_escopo")


def test_previsao_a_print_nao_e_return():
    assert ex.previsao_a() == ["10", "None"], (
        "Uma função sem return devolve None, mesmo que tenha dado print."
    )


def test_previsao_b_variavel_local_nao_muda_a_global():
    assert ex.previsao_b() == 0


def test_previsao_c_padrao_mutavel_acumula():
    assert ex.previsao_c() == ["bolha", "risco", "gel"]


def test_previsao_d_reatribuir_x_modificar():
    assert ex.previsao_d() == ([1, 2], [])


def test_resumo_lote_devolve_tupla():
    assert ex.resumo_lote([50.2, 44.1, 56.3, 49.9], 45.0, 55.0) == ([44.1, 56.3], 50.0)


def test_resumo_lote_percentual_com_uma_casa():
    fora, pct = ex.resumo_lote([10.0, 50.0, 50.0], 45.0, 55.0)
    assert fora == [10.0]
    assert pct == pytest.approx(33.3)


def test_resumo_lote_chamadas_nao_interferem():
    ex.resumo_lote([10.0, 99.0], 45.0, 55.0)
    fora, pct = ex.resumo_lote([50.0, 60.0], 45.0, 55.0)
    assert fora == [60.0], "A segunda chamada 'lembrou' a primeira: padrão mutável?"
    assert pct == 50.0


def test_resumo_lote_lista_vazia():
    assert ex.resumo_lote([], 45.0, 55.0) == ([], 0.0)


def test_resumo_lote_nao_imprime_nada(capsys):
    ex.resumo_lote([50.0, 60.0], 45.0, 55.0)
    assert capsys.readouterr().out == "", "Função pura: devolva o resultado, não dê print."
