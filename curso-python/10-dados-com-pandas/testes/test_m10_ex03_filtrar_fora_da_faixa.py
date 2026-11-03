import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex03_filtrar_fora_da_faixa")


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "bobina": ["024412-01", "024412-02", "024413-01", "024420-01", "024420-02"],
            "linha": ["A", "A", "B", "C", "C"],
            "espessura_um": [38.1, 44.5, 35.0, 36.0, 44.0],
        }
    )


def test_fora_da_faixa_pega_acima_e_abaixo(df):
    resultado = ex.fora_da_faixa(df, "espessura_um", 36.5, 44.0)
    esperado = pd.DataFrame(
        {"bobina": ["024412-02", "024413-01", "024420-01"], "linha": ["A", "B", "C"],
         "espessura_um": [44.5, 35.0, 36.0]}
    )  # fmt: skip
    assert_frame_equal(resultado, esperado)


def test_limites_estao_dentro_da_faixa(df):
    resultado = ex.fora_da_faixa(df, "espessura_um", 36.0, 44.0)
    assert resultado["bobina"].tolist() == ["024412-02", "024413-01"], (
        "36.0 e 44.0 são exatamente os limites: estão DENTRO da faixa"
    )


def test_indice_renumerado(df):
    resultado = ex.fora_da_faixa(df, "espessura_um", 36.0, 44.0)
    assert resultado.index.tolist() == [0, 1], "use reset_index(drop=True)"


def test_nada_fora_devolve_tabela_vazia_com_as_colunas(df):
    resultado = ex.fora_da_faixa(df, "espessura_um", 0, 100)
    assert len(resultado) == 0
    assert list(resultado.columns) == ["bobina", "linha", "espessura_um"]


def test_nao_altera_o_original(df):
    copia = df.copy()
    ex.fora_da_faixa(df, "espessura_um", 36.0, 44.0)
    ex.filtrar_linhas(df, ["A"])
    assert_frame_equal(df, copia)


@pytest.mark.parametrize(
    ("linhas", "bobinas"),
    [
        (["A"], ["024412-01", "024412-02"]),
        (["C", "A"], ["024412-01", "024412-02", "024420-01", "024420-02"]),
        (["D"], []),
    ],
)
def test_filtrar_linhas(df, linhas, bobinas):
    resultado = ex.filtrar_linhas(df, linhas)
    assert resultado["bobina"].tolist() == bobinas
    assert resultado.index.tolist() == list(range(len(bobinas)))
