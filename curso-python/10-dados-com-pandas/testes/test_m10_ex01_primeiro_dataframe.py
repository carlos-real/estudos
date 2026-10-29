import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from _curso import carregar

ex = carregar(__file__, "ex01_primeiro_dataframe")


def test_cria_tabela_com_colunas_na_ordem():
    tabela = ex.criar_tabela_bobinas(["024412-01", "024412-02"], [1250.5, 980.0])
    esperado = pd.DataFrame({"bobina": ["024412-01", "024412-02"], "peso_kg": [1250.5, 980.0]})
    assert_frame_equal(tabela, esperado)


def test_listas_de_tamanhos_diferentes_dao_value_error():
    with pytest.raises(ValueError):
        ex.criar_tabela_bobinas(["024412-01", "024412-02"], [1250.5])


def test_peso_total():
    tabela = ex.criar_tabela_bobinas(["a", "b", "c"], [1250.5, 980.0, 1100.0])
    assert ex.peso_total(tabela) == pytest.approx(3330.5)
    assert isinstance(ex.peso_total(tabela), float), "devolva um float (use float(...))"


def test_peso_total_de_tabela_vazia_e_zero():
    vazia = pd.DataFrame({"bobina": [], "peso_kg": []})
    assert ex.peso_total(vazia) == 0.0


@pytest.mark.parametrize(
    ("pesos", "esperada"),
    [
        ([980.0, 1250.5, 1100.0], "b"),
        ([1300.0, 1250.5, 1100.0], "a"),
        ([900.0, 1250.5, 1250.5], "b"),  # empate: vale a primeira
    ],
)
def test_bobina_mais_pesada(pesos, esperada):
    tabela = pd.DataFrame({"bobina": ["a", "b", "c"], "peso_kg": pesos})
    assert ex.bobina_mais_pesada(tabela) == esperada
