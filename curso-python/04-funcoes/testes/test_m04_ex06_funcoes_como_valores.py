import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_funcoes_como_valores")

MEDICOES = [50.2, 44.1, 56.3, 49.9, 55.0]


def acima_de_50(valor):
    return valor > 50


def test_cont_se_com_lambda():
    assert ex.cont_se(MEDICOES, lambda v: v < 45) == 1


def test_cont_se_com_funcao_def():
    assert ex.cont_se(MEDICOES, acima_de_50) == 3


def test_cont_se_nenhum_e_lista_vazia():
    assert ex.cont_se(MEDICOES, lambda v: v > 100) == 0
    assert ex.cont_se([], acima_de_50) == 0


def test_soma_se():
    assert ex.soma_se([500.0, 320.5, 80.0], lambda p: p >= 100) == pytest.approx(820.5)


def test_soma_se_arredonda_e_devolve_zero_sem_valores():
    assert ex.soma_se([0.1, 0.2], lambda v: True) == 0.3, "Use round(..., 2)."
    assert ex.soma_se([1.0, 2.0], lambda v: False) == 0.0


def test_verificador_devolve_uma_funcao():
    dentro = ex.criar_verificador_faixa(45.0, 55.0)
    assert callable(dentro), "Devolva a função (sem parênteses), não o resultado dela."


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(50.2, True), (45.0, True), (55.0, True), (44.9, False), (56.3, False)],
)
def test_verificador_confere_a_faixa(valor, esperado):
    dentro = ex.criar_verificador_faixa(45.0, 55.0)
    assert dentro(valor) is esperado


def test_verificadores_sao_independentes():
    linha_a = ex.criar_verificador_faixa(45.0, 55.0)
    linha_b = ex.criar_verificador_faixa(18.0, 22.0)
    assert linha_a(50.0) is True
    assert linha_b(50.0) is False, "Cada verificador deve lembrar a SUA faixa."


def test_verificador_combinado_com_cont_se():
    assert ex.cont_se(MEDICOES, ex.criar_verificador_faixa(45.0, 55.0)) == 3
