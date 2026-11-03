import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.axes import Axes

from _curso import carregar

matplotlib.use("Agg")
ex = carregar(__file__, "ex12_grafico_controle")

REFERENCIA = pd.Series([61.8, 62.3, 61.5, 62.0, 62.4])  # média 62.0, σ ≈ 0.3674
VIGIADOS = pd.Series([62.1, 63.5, 61.9, 60.0, 62.2])  # 63.5 e 60.0 estão fora


# Limites "de mão" (média 62.0, σ ≈ 0.3674): assim os testes do gráfico e dos
# pontos fora não dependem de limites_de_controle estar certa.
LIMITES = {"media": 62.0, "lic": 60.8977, "lsc": 63.1023}


@pytest.fixture(autouse=True)
def fechar_figuras():
    yield
    plt.close("all")


def test_limites():
    limites = ex.limites_de_controle(REFERENCIA)
    assert limites["media"] == pytest.approx(62.0)
    assert limites["lic"] == pytest.approx(62.0 - 3 * 0.367423, abs=1e-4)
    assert limites["lsc"] == pytest.approx(62.0 + 3 * 0.367423, abs=1e-4)


def test_limites_usam_desvio_amostral():
    limites = ex.limites_de_controle(pd.Series([1.0, 3.0]))
    # desvio amostral de [1, 3] = 1.4142 (o populacional seria 1.0)
    assert limites["lsc"] == pytest.approx(2.0 + 3 * 1.414214, abs=1e-4)


@pytest.mark.parametrize("poucos", [pd.Series([62.0]), pd.Series([], dtype=float)])
def test_menos_de_dois_valores_da_value_error(poucos):
    with pytest.raises(ValueError):
        ex.limites_de_controle(poucos)


def test_pontos_fora():
    limites = dict(LIMITES)
    assert ex.pontos_fora_de_controle(VIGIADOS, limites) == [1, 3]


def test_pontos_fora_usa_posicoes_mesmo_com_indice_estranho():
    limites = dict(LIMITES)
    filtrada = pd.Series([62.1, 63.5, 62.0], index=[10, 25, 40])
    assert ex.pontos_fora_de_controle(filtrada, limites) == [1]


def test_nenhum_ponto_fora():
    limites = dict(LIMITES)
    assert ex.pontos_fora_de_controle(REFERENCIA, limites) == []


def test_grafico_tem_titulo_e_rotulos():
    limites = dict(LIMITES)
    ax = ex.grafico_controle(VIGIADOS, limites, "Espessura LAM-62")
    assert isinstance(ax, Axes)
    assert ax.get_title() == "Espessura LAM-62"
    assert ax.get_xlabel() == "Amostra"
    assert ax.get_ylabel() == "Valor"


def test_grafico_tem_quatro_linhas_com_os_limites():
    limites = dict(LIMITES)
    ax = ex.grafico_controle(VIGIADOS, limites, "x")
    linhas = ax.get_lines()
    assert len(linhas) == 4, "1 linha de valores + média + LIC + LSC"
    horizontais = sorted(
        linha.get_ydata()[0] for linha in linhas if len(set(linha.get_ydata())) == 1
    )
    assert horizontais == pytest.approx([limites["lic"], limites["media"], limites["lsc"]])


def test_linha_de_valores_comeca_na_amostra_1():
    limites = dict(LIMITES)
    ax = ex.grafico_controle(VIGIADOS, limites, "x")
    dados = max(ax.get_lines(), key=lambda linha: len(linha.get_xdata()))
    assert list(dados.get_xdata()) == [1, 2, 3, 4, 5]
    assert list(dados.get_ydata()) == pytest.approx(VIGIADOS.tolist())


def test_pontos_fora_destacados():
    limites = dict(LIMITES)
    ax = ex.grafico_controle(VIGIADOS, limites, "x")
    destacados = sum(len(colecao.get_offsets()) for colecao in ax.collections)
    assert destacados == 2, "destaque os 2 pontos fora com ax.scatter"


def test_sem_pontos_fora_nada_destacado():
    limites = dict(LIMITES)
    ax = ex.grafico_controle(REFERENCIA, limites, "x")
    destacados = sum(len(colecao.get_offsets()) for colecao in ax.collections)
    assert destacados == 0
