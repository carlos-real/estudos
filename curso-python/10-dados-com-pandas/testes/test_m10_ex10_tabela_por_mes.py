import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex10_tabela_por_mes")


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "linha": ["B", "A", "A", "B", "A", "C"],
            "data": ["20/07/2026", "03/07/2026", "15/08/2026", "02/07/2026", "31/07/2026",
                     "01/09/2026"],
            "peso_kg": [1310.2, 1558.5, 980.0, 700.04, 1000.0, 845.0],
        }
    )  # fmt: skip


def test_adicionar_mes(df):
    resultado = ex.adicionar_mes(df)
    assert resultado["mes"].tolist() == [
        "2026-07", "2026-07", "2026-08", "2026-07", "2026-07", "2026-09"
    ]  # fmt: skip


def test_adicionar_mes_entende_dia_primeiro():
    df = pd.DataFrame({"data": ["03/07/2026", "12/01/2027"]})
    assert ex.adicionar_mes(df)["mes"].tolist() == ["2026-07", "2027-01"], (
        "03/07/2026 é 3 de julho: use format='%d/%m/%Y'"
    )


def test_adicionar_mes_nao_altera_o_original(df):
    copia = df.copy()
    ex.adicionar_mes(df)
    assert_frame_equal(df, copia)


@pytest.mark.parametrize("data_ruim", ["31/09/2026", "2026-07-03", None])
def test_data_invalida_ou_vazia_da_value_error(data_ruim):
    df = pd.DataFrame({"data": ["03/07/2026", data_ruim]})
    with pytest.raises(ValueError):
        ex.adicionar_mes(df)


def test_tabela_dinamica_completa(df):
    resultado = ex.peso_por_linha_e_mes(df)
    esperado = pd.DataFrame(
        {
            "2026-07": [2558.5, 2010.2, 0.0],
            "2026-08": [980.0, 0.0, 0.0],
            "2026-09": [0.0, 0.0, 845.0],
        },
        index=pd.Index(["A", "B", "C"], name="linha"),
    )
    esperado.columns.name = "mes"
    assert_frame_equal(resultado, esperado, check_dtype=False)


def test_tabela_sem_buracos(df):
    resultado = ex.peso_por_linha_e_mes(df)
    assert resultado.isna().sum().sum() == 0, "use fill_value=0 na pivot_table"
