import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex08_resumo_por_linha")


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "linha": ["B", "A", "A", "A", "D", "D"],
            "bobina": ["b1", "a1", "a2", "a3", "d1", "d2"],
            "espessura_um": [35.3, 38.1, 39.6, 40.4, 61.8, 58.9],
            "peso_kg": [1310.2, 1250.5, 980.0, 1100.0, 1180.44, 1325.0],
            "cof": [0.37, 0.21, 0.24, 0.27, 0.19, 0.20],
        }
    )


def test_resumo_completo(df):
    resultado = ex.resumo_por_linha(df)
    esperado = pd.DataFrame(
        {
            "linha": ["A", "B", "D"],
            "bobinas": [3, 1, 2],
            "peso_total_kg": [3330.5, 1310.2, 2505.4],
            "espessura_media": [39.37, 35.3, 60.35],
            "espessura_desvio": [1.17, np.nan, 2.05],
            "cof_max": [0.27, 0.37, 0.20],
        }
    )
    assert_frame_equal(resultado, esperado, check_dtype=False)


def test_colunas_na_ordem(df):
    resultado = ex.resumo_por_linha(df)
    assert list(resultado.columns) == [
        "linha", "bobinas", "peso_total_kg", "espessura_media", "espessura_desvio", "cof_max"
    ]  # fmt: skip


def test_linhas_em_ordem_alfabetica_com_indice_novo(df):
    resultado = ex.resumo_por_linha(df)
    assert resultado["linha"].tolist() == ["A", "B", "D"]
    assert resultado.index.tolist() == [0, 1, 2], "use as_index=False ou reset_index()"


def test_desvio_e_amostral(df):
    resultado = ex.resumo_por_linha(df)
    desvio_a = resultado.loc[resultado["linha"] == "A", "espessura_desvio"].iloc[0]
    assert desvio_a == pytest.approx(1.17), "desvio-padrão AMOSTRAL (o .std() do pandas)"


def test_uma_linha_so():
    df = pd.DataFrame(
        {"linha": ["C"], "bobina": ["c1"], "espessura_um": [70.0], "peso_kg": [900.0],
         "cof": [0.2]}
    )  # fmt: skip
    resultado = ex.resumo_por_linha(df)
    assert len(resultado) == 1
    assert resultado.loc[0, "bobinas"] == 1
    assert np.isnan(resultado.loc[0, "espessura_desvio"])
