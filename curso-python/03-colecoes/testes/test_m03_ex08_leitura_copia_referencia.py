import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_leitura_copia_referencia")


def test_previsao_trecho_a_atribuicao_nao_copia():
    assert ex.previsao_a() == [50.2, 49.8, 51.0], (
        "b = a não cria uma lista nova: os dois nomes apontam para o mesmo objeto."
    )


def test_previsao_trecho_b_copy_cria_lista_nova():
    assert ex.previsao_b() == [50.2, 49.8]


def test_previsao_trecho_c_copia_rasa():
    assert ex.previsao_c() == [50.2, 49.9], (
        "dict.copy() é cópia rasa: as listas dentro do dicionário continuam compartilhadas."
    )


def test_previsao_trecho_d_remover_durante_o_for():
    assert ex.previsao_d() == [10, 60, 20], (
        "Remover itens enquanto o for percorre a lista faz o laço pular elementos."
    )


def test_corrigir_offset_calcula_os_valores():
    assert ex.corrigir_offset([50.4, 49.9], 0.2) == pytest.approx([50.2, 49.7])


def test_corrigir_offset_arredonda_em_duas_casas():
    assert ex.corrigir_offset([0.3], 0.1) == [0.2], "Use round(..., 2): 0.3 - 0.1 não dá 0.2."


def test_corrigir_offset_nao_altera_a_lista_original():
    medicoes = [50.4, 49.9, 51.0]
    resultado = ex.corrigir_offset(medicoes, 0.4)
    assert medicoes == [50.4, 49.9, 51.0], "A lista original foi alterada: monte uma nova."
    assert resultado is not medicoes


def test_corrigir_offset_de_lista_vazia():
    assert ex.corrigir_offset([], 0.5) == []
