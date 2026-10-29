import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_tolerancia_fixa")


@pytest.mark.parametrize("valor", [0.15, 0.22, 0.35])
def test_dentro_da_faixa_e_nos_limites(valor):
    assert ex.verificar_fixa("cof", valor, 0.15, 0.35) is None, (
        "Os limites são inclusivos: o valor igual ao limite passa."
    )


def test_acima_do_maximo():
    assert ex.verificar_fixa("cof", 0.38, 0.15, 0.35) == "cof 0.38 acima do máximo 0.35"


def test_abaixo_do_minimo():
    assert ex.verificar_fixa("cof", 0.12, 0.15, 0.35) == "cof 0.12 abaixo do mínimo 0.15"


def test_numeros_formatados_com_g():
    assert ex.verificar_fixa("selagem", 7.6, 8.0, None) == "selagem 7.6 abaixo do mínimo 8"
    assert ex.verificar_fixa("cof", 0.4, 0.2, 0.30) == "cof 0.4 acima do máximo 0.3"


@pytest.mark.parametrize(
    ("valor", "minimo", "maximo"),
    [(999.0, 20.0, None), (0.0, None, 0.35), (-5.0, None, 0.35)],
)
def test_lado_sem_limite_nao_reprova(valor, minimo, maximo):
    assert ex.verificar_fixa("x", valor, minimo, maximo) is None


def test_so_minimo_ainda_reprova_abaixo():
    assert ex.verificar_fixa("tracao", 18.7, 20.0, None) == "tracao 18.7 abaixo do mínimo 20"
