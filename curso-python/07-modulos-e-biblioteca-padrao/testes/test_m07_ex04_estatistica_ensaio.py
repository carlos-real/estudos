import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_estatistica_ensaio")

ESPESSURAS = [25.1, 24.8, 25.3, 24.9, 25.4, 25.0]


def test_cv_das_espessuras():
    assert ex.coeficiente_variacao(ESPESSURAS) == pytest.approx(0.92)


@pytest.mark.parametrize(
    ("valores", "esperado"),
    [
        ([10.0, 12.0], 12.86),
        ([0.21, 0.28, 0.19, 0.25], 17.34),
        ([40.0, 40.0, 40.0], 0.0),
    ],
)
def test_cv_outros_casos(valores, esperado):
    assert ex.coeficiente_variacao(valores) == pytest.approx(esperado), (
        "Use o desvio AMOSTRAL (statistics.stdev), não o populacional (pstdev)."
    )


@pytest.mark.parametrize("valores", [[], [25.0]])
def test_cv_com_menos_de_dois_valores(valores):
    with pytest.raises(ValueError):
        ex.coeficiente_variacao(valores)


def test_cv_com_media_zero():
    with pytest.raises(ValueError):
        ex.coeficiente_variacao([-1.0, 1.0])


def test_resumo_completo():
    resumo = ex.resumo_ensaio(ESPESSURAS)
    assert resumo == {
        "n": 6,
        "media": pytest.approx(25.083),
        "mediana": pytest.approx(25.05),
        "desvio": pytest.approx(0.232),
        "minimo": pytest.approx(24.8),
        "maximo": pytest.approx(25.4),
        "cv": pytest.approx(0.92),
    }


def test_resumo_tem_exatamente_as_chaves_pedidas():
    chaves = set(ex.resumo_ensaio([10.0, 12.0]))
    assert chaves == {"n", "media", "mediana", "desvio", "minimo", "maximo", "cv"}


def test_resumo_mediana_com_quantidade_impar():
    resumo = ex.resumo_ensaio([3.0, 100.0, 4.0])
    assert resumo["mediana"] == pytest.approx(4.0)
    assert resumo["n"] == 3


def test_resumo_com_um_valor_gera_value_error():
    with pytest.raises(ValueError):
        ex.resumo_ensaio([25.0])
