import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from _curso import carregar

ex = carregar(__file__, "ex07_corrija_o_relatorio")


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "linha": ["A", "A", "A", "A", "B", "B", "C", "C", "D"],
            "bobina": ["a1", "a2", "a3", "a4", "b1", "b2", "c1", "c2", "d1"],
            "cof": [0.38, 0.30, 0.36, 0.20, 0.25, 0.41, 0.22, 0.35, 0.10],
        }
    )


def test_percentuais_corretos(df):
    resultado = ex.percentual_cof_alto(df, 0.35)
    assert resultado["A"] == pytest.approx(50.0)
    assert resultado["B"] == pytest.approx(50.0)
    assert resultado["C"] == pytest.approx(0.0), "0.35 não é MAIOR que 0.35"


def test_linha_sem_cof_alto_aparece_com_zero(df):
    resultado = ex.percentual_cof_alto(df, 0.35)
    assert "D" in resultado.index, "a linha D sumiu: defeito (2)"
    assert resultado["D"] == 0.0, "linha sem bobina alta deve dar 0.0, não NaN"
    assert resultado.isna().sum() == 0


def test_serie_completa_ordenada_piores_primeiro(df):
    resultado = ex.percentual_cof_alto(df, 0.35)
    esperado = pd.Series(
        [50.0, 50.0, 0.0, 0.0],
        index=pd.Index(["A", "B", "C", "D"], name="linha"),
        name="pct_cof_alto",
    )
    assert_series_equal(resultado, esperado)


def test_ordem_decrescente_com_empate_alfabetico():
    df = pd.DataFrame(
        {"linha": ["D", "B", "B", "A", "C"], "bobina": ["d", "b1", "b2", "a", "c"],
         "cof": [0.50, 0.50, 0.10, 0.50, 0.10]}
    )  # fmt: skip
    resultado = ex.percentual_cof_alto(df, 0.35)
    assert resultado.index.tolist() == ["A", "D", "B", "C"]
    assert resultado.tolist() == [100.0, 100.0, 50.0, 0.0]


def test_arredonda_em_uma_casa():
    df = pd.DataFrame({"linha": ["A"] * 3, "bobina": ["1", "2", "3"], "cof": [0.5, 0.1, 0.1]})
    assert ex.percentual_cof_alto(df, 0.35)["A"] == pytest.approx(33.3)


def test_nao_altera_o_dataframe_recebido(df):
    copia = df.copy()
    ex.percentual_cof_alto(df, 0.35)
    assert_frame_equal(df, copia, obj="o DataFrame recebido (defeito 4)")
