import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_sequencia_fora")


@pytest.mark.parametrize(
    ("valores", "tamanho", "esperado"),
    [
        ([25, 22, 21, 20, 25], 3, 2),
        ([22, 25, 21, 20, 19], 3, 3),
        ([20, 20, 25, 20, 20, 20], 3, 4),
        ([1, 1, 1], 3, 1),
        ([20, 20, 20, 20, 20], 2, 1),
    ],
)
def test_encontra_inicio_da_sequencia(valores, tamanho, esperado):
    resultado = ex.inicio_sequencia_fora(valores, 23, 27, tamanho)
    assert resultado == esperado, (
        f"inicio_sequencia_fora({valores}, 23, 27, {tamanho}) devolveu {resultado!r}; "
        f"esperado {esperado}."
    )


@pytest.mark.parametrize(
    "valores",
    [
        [22, 25, 21, 20, 25],
        [25, 24, 26],
        [23, 27, 23],
        [],
    ],
)
def test_sem_sequencia_devolve_zero(valores):
    resultado = ex.inicio_sequencia_fora(valores, 23, 27, 3)
    assert resultado == 0, (
        f"Em {valores} não há 3 seguidas fora de [23, 27] (limites são DENTRO); "
        f"deu {resultado!r}."
    )


def test_tamanho_um_devolve_primeira_fora():
    assert ex.inicio_sequencia_fora([25, 28, 25], 23, 27, 1) == 2


def test_medicao_boa_zera_a_contagem():
    # 2 fora, 1 boa, 2 fora: nunca chega a 3 seguidas
    assert ex.inicio_sequencia_fora([20, 20, 25, 20, 20], 23, 27, 3) == 0
