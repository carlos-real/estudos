import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.axes import Axes

from _curso import carregar

matplotlib.use("Agg")  # desenha só na memória, sem abrir janelas
ex = carregar(__file__, "ex11_grafico_barras")


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "linha": ["B", "A", "A", "D", "B"],
            "peso_kg": [1310.2, 1250.5, 980.0, 1500.0, 700.0],
        }
    )


@pytest.fixture(autouse=True)
def fechar_figuras():
    yield
    plt.close("all")


def test_devolve_um_axes(df):
    ax = ex.grafico_peso_por_linha(df)
    assert isinstance(ax, Axes), "devolva o Axes (ex.: o retorno de .plot.bar)"


def test_uma_barra_por_linha(df):
    ax = ex.grafico_peso_por_linha(df)
    assert len(ax.patches) == 3, "são 3 linhas de produção: A, B e D"


def test_altura_das_barras_em_toneladas(df):
    ax = ex.grafico_peso_por_linha(df)
    alturas = [barra.get_height() for barra in ax.patches]
    assert alturas == pytest.approx([2.2305, 2.0102, 1.5]), "some por linha e divida por 1000"


def test_rotulos_das_barras_em_ordem(df):
    ax = ex.grafico_peso_por_linha(df)
    ax.figure.canvas.draw()  # garante que os rótulos foram calculados
    rotulos = [texto.get_text() for texto in ax.get_xticklabels()]
    assert rotulos == ["A", "B", "D"]


def test_titulo_e_eixos(df):
    ax = ex.grafico_peso_por_linha(df)
    assert ax.get_title() == "Peso medido por linha"
    assert ax.get_xlabel() == "Linha"
    assert ax.get_ylabel() == "Peso (t)"


def test_salvar_png_cria_pasta_e_arquivo(df, tmp_path):
    ax = ex.grafico_peso_por_linha(df)
    destino = tmp_path / "relatorio" / "graficos" / "peso.png"
    devolvido = ex.salvar_png(ax, destino)
    assert devolvido == destino
    assert destino.exists(), "crie a pasta com mkdir(parents=True, exist_ok=True)"
    assert destino.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", "o arquivo precisa ser um PNG"
