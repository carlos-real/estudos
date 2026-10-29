import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex04_nova_coluna_desvio")


@pytest.fixture
def df():
    return pd.DataFrame(
        {"bobina": ["01", "02", "03", "04"], "espessura_um": [61.8, 67.5, 57.66, 62.0]}
    )


def test_adicionar_desvio_calcula_as_duas_colunas(df):
    resultado = ex.adicionar_desvio(df, 62.0)
    assert list(resultado.columns) == ["bobina", "espessura_um", "desvio_um", "desvio_pct"]
    assert resultado["desvio_um"].tolist() == pytest.approx([-0.2, 5.5, -4.34, 0.0])
    assert resultado["desvio_pct"].tolist() == pytest.approx([-0.32, 8.87, -7.0, 0.0])


def test_adicionar_desvio_arredonda_em_duas_casas():
    df = pd.DataFrame({"bobina": ["x"], "espessura_um": [40.123]})
    resultado = ex.adicionar_desvio(df, 40.0)
    assert resultado.loc[0, "desvio_um"] == pytest.approx(0.12)
    assert resultado.loc[0, "desvio_pct"] == pytest.approx(0.31)


def test_adicionar_desvio_nao_altera_o_original(df):
    copia = df.copy()
    ex.adicionar_desvio(df, 62.0)
    assert_frame_equal(df, copia, obj="o DataFrame recebido (use df.copy())")


def test_classificar_com_limite_inclusivo(df):
    com_desvio = ex.adicionar_desvio(df, 62.0)
    resultado = ex.classificar(com_desvio, 7.0)
    assert resultado["status"].tolist() == ["APROVADA", "REPROVADA", "APROVADA", "APROVADA"], (
        "57.66 está exatamente a -7%: ainda é APROVADA"
    )


def test_classificar_nao_altera_o_original():
    df = pd.DataFrame({"bobina": ["01", "02"], "desvio_pct": [1.0, -9.5]})
    copia = df.copy()
    resultado = ex.classificar(df, 5.0)
    assert resultado["status"].tolist() == ["APROVADA", "REPROVADA"]
    assert_frame_equal(df, copia, obj="o DataFrame recebido (use df.copy())")
