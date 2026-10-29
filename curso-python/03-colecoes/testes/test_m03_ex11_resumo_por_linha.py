import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_resumo_por_linha")

AMOSTRAS = [
    {"op": "OP-4512", "linha": "B", "espessura": 20.9, "cof": 0.25},
    {"op": "OP-4513", "linha": "A", "espessura": 50.4, "cof": 0.21},
    {"op": "OP-4514", "linha": "A", "espessura": 49.7},
    {"op": "OP-4515", "linha": "A", "espessura": None, "cof": 0.30},
    {"op": "OP-4516", "linha": "C"},
    {"op": "OP-4517", "linha": "B", "espessura": 19.5},
]


def test_agrupa_valores_por_linha_na_ordem_de_aparicao():
    assert ex.agrupar_valores(AMOSTRAS, "espessura") == {"B": [20.9, 19.5], "A": [50.4, 49.7]}


def test_agrupar_ignora_campo_ausente_ou_none():
    grupos = ex.agrupar_valores(AMOSTRAS, "cof")
    assert grupos == {"B": [0.25], "A": [0.21, 0.30]}, (
        "Amostras sem o campo (ou com None) não entram; a linha C não deve aparecer."
    )


def test_agrupar_tabela_vazia():
    assert ex.agrupar_valores([], "espessura") == {}


def test_resumo_de_cada_linha():
    resumo = ex.resumo_por_linha(AMOSTRAS, "espessura")
    assert resumo["A"]["qtd"] == 2
    assert resumo["A"]["media"] == pytest.approx(50.05)
    assert resumo["A"]["minimo"] == 49.7
    assert resumo["A"]["maximo"] == 50.4
    assert resumo["B"] == {"qtd": 2, "media": 20.2, "minimo": 19.5, "maximo": 20.9}


def test_resumo_em_ordem_alfabetica_de_linha():
    resumo = ex.resumo_por_linha(AMOSTRAS, "espessura")
    assert list(resumo) == ["A", "B"], "As linhas devem sair em ordem alfabética."


def test_resumo_sem_linhas_vazias():
    resumo = ex.resumo_por_linha(AMOSTRAS, "espessura")
    assert "C" not in resumo, "A linha C não tem nenhum valor de espessura."


def test_media_arredondada():
    amostras = [{"linha": "D", "gramatura": g} for g in (46.0, 46.1, 46.1)]
    assert ex.resumo_por_linha(amostras, "gramatura")["D"]["media"] == 46.07


def test_resumo_de_tabela_vazia():
    assert ex.resumo_por_linha([], "espessura") == {}
