import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex09_conferir_especificacao")


@pytest.fixture
def specs():
    return pd.DataFrame(
        {
            "produto": ["PE-40", "LAM-62", "COEX-70"],
            "descricao": ["Filme PE 40", "Laminado PET/PE", "Coextrusado"],
            "nominal_um": [40.0, 62.0, 70.0],
            "tolerancia_pct": [10.0, 7.0, 8.0],
        }
    )


@pytest.fixture
def medicoes():
    return pd.DataFrame(
        {
            "bobina": ["01", "02", "03", "04", "05"],
            "produto": ["LAM-62", "PE-40", "PE-90", "LAM-62", "PE-40"],
            "espessura_um": [67.5, 38.1, 94.4, 57.66, 35.9],
        }
    )


def test_resultado_completo(medicoes, specs):
    resultado = ex.conferir_espessura(medicoes, specs)
    esperado = pd.DataFrame(
        {
            "bobina": ["01", "02", "03", "04", "05"],
            "produto": ["LAM-62", "PE-40", "PE-90", "LAM-62", "PE-40"],
            "espessura_um": [67.5, 38.1, 94.4, 57.66, 35.9],
            "minimo": [57.66, 36.0, np.nan, 57.66, 36.0],
            "maximo": [66.34, 44.0, np.nan, 66.34, 44.0],
            "status": ["REPROVADA", "APROVADA", "SEM ESPECIFICAÇÃO", "APROVADA", "REPROVADA"],
        }
    )
    assert_frame_equal(resultado, esperado, check_dtype=False)


def test_nenhuma_medicao_some(medicoes, specs):
    resultado = ex.conferir_espessura(medicoes, specs)
    assert resultado["bobina"].tolist() == ["01", "02", "03", "04", "05"], (
        "use how='left' para não perder medições sem especificação"
    )


def test_limite_exato_e_aprovado(medicoes, specs):
    resultado = ex.conferir_espessura(medicoes, specs)
    assert resultado.loc[3, "status"] == "APROVADA", "57.66 é o mínimo exato do LAM-62"


def test_sem_especificacao_nao_e_reprovada(medicoes, specs):
    resultado = ex.conferir_espessura(medicoes, specs)
    linha = resultado[resultado["produto"] == "PE-90"].iloc[0]
    assert linha["status"] == "SEM ESPECIFICAÇÃO"
    assert np.isnan(linha["minimo"]) and np.isnan(linha["maximo"])


def test_colunas_auxiliares_nao_aparecem(medicoes, specs):
    resultado = ex.conferir_espessura(medicoes, specs)
    assert list(resultado.columns) == [
        "bobina", "produto", "espessura_um", "minimo", "maximo", "status"
    ]  # fmt: skip


def test_especificacao_duplicada_da_value_error(medicoes, specs):
    duplicada = pd.concat([specs, specs.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError):
        ex.conferir_espessura(medicoes, duplicada)


def test_nao_altera_as_tabelas_recebidas(medicoes, specs):
    copia_m, copia_s = medicoes.copy(), specs.copy()
    ex.conferir_espessura(medicoes, specs)
    assert_frame_equal(medicoes, copia_m)
    assert_frame_equal(specs, copia_s)
