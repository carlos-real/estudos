import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex06_limpar_medicoes")


def tabela_texto(linhas):
    colunas = ["op", "linha", "bobina", "espessura_um", "peso_kg"]
    return pd.DataFrame(linhas, columns=colunas, dtype=str)


@pytest.fixture
def bruto():
    return tabela_texto(
        [
            ["024470", "A", "024470-01", "51,2", "1.120,5"],
            ["024470", " a", "024470-02", "49,8", "1.098,0"],
            ["024470", "A", "024470-02", "49,8", "1.098,0"],
            ["024470", "A ", "024470-03", "n/d", "1.205,3"],
            ["024474", "c", "024474-01", "71,3", "845,0"],
            ["024474", "C", "024474-02", None, "910,2"],
            ["024474", "C", "024474-03", "69,9", None],
            ["024479", "b", "024479-02", " 34,7 ", "1.288,4"],
        ]
    )


def test_resultado_completo(bruto):
    resultado = ex.limpar_medicoes(bruto)
    esperado = pd.DataFrame(
        {
            "op": ["024470", "024470", "024474", "024474", "024479"],
            "linha": ["A", "A", "C", "C", "B"],
            "bobina": ["024470-01", "024470-02", "024474-01", "024474-03", "024479-02"],
            "espessura_um": [51.2, 49.8, 71.3, 69.9, 34.7],
            "peso_kg": [1120.5, 1098.0, 845.0, np.nan, 1288.4],
        }
    )
    assert_frame_equal(resultado, esperado, check_dtype=False)


def test_linha_padronizada(bruto):
    resultado = ex.limpar_medicoes(bruto)
    assert sorted(resultado["linha"].unique()) == ["A", "B", "C"]


def test_numeros_brasileiros_viram_float(bruto):
    resultado = ex.limpar_medicoes(bruto)
    assert resultado["peso_kg"].dtype == "float64", "peso_kg precisa ser número"
    assert resultado["espessura_um"].dtype == "float64", "espessura_um precisa ser número"
    assert resultado.loc[0, "peso_kg"] == pytest.approx(1120.5), "'1.120,5' vale 1120.5"


def test_descarta_sem_espessura_mas_mantem_sem_peso(bruto):
    resultado = ex.limpar_medicoes(bruto)
    assert "024470-03" not in resultado["bobina"].tolist(), "'n/d' não é medida"
    assert "024474-02" not in resultado["bobina"].tolist(), "vazio não é medida"
    assert "024474-03" in resultado["bobina"].tolist(), "peso vazio NÃO descarta a linha"


def test_bobina_repetida_fica_a_primeira(bruto):
    resultado = ex.limpar_medicoes(bruto)
    assert resultado["bobina"].tolist().count("024470-02") == 1


def test_indice_e_original(bruto):
    copia = bruto.copy()
    resultado = ex.limpar_medicoes(bruto)
    assert resultado.index.tolist() == list(range(len(resultado)))
    assert_frame_equal(bruto, copia, obj="a tabela recebida (use .copy())")
