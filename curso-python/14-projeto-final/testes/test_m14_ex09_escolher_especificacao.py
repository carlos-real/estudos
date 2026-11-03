import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_escolher_especificacao")


@pytest.fixture
def especificacoes():
    T = ex.Tolerancia
    return {
        "PADRAO-A": ex.Especificacao(
            "PADRAO-A",
            linha="A",
            tolerancias={
                "espessura": T("espessura", "nominal", percentual=10.0),
                "cof": T("cof", "fixa", minimo=0.15, maximo=0.35),
            },
        ),
        "PADRAO-C": ex.Especificacao(
            "PADRAO-C",
            linha="C",
            tolerancias={
                "espessura": T("espessura", "nominal", percentual=8.0),
                "cof": T("cof", "fixa", minimo=0.10, maximo=0.30),
                "selagem": T("selagem", "fixa", minimo=10.0),
            },
        ),
        "ESP-0412": ex.Especificacao(
            "ESP-0412",
            texto="Café 250 g",
            tolerancias={
                "cof": T("cof", "fixa", minimo=0.18, maximo=0.25),
                "selagem": T("selagem", "fixa", minimo=12.0),
            },
        ),
    }


@pytest.mark.parametrize("titulo", [None, "", "   "])
def test_sem_titulo_usa_padrao_da_linha(especificacoes, titulo):
    escolhida = ex.escolher_especificacao(titulo, "A", especificacoes)
    assert escolhida.titulo == "PADRAO-A"


def test_padrao_e_da_linha_certa(especificacoes):
    assert ex.escolher_especificacao("", "C", especificacoes).titulo == "PADRAO-C"


def test_titulo_do_cliente_herda_do_padrao(especificacoes):
    escolhida = ex.escolher_especificacao("ESP-0412", "C", especificacoes)
    assert escolhida.titulo == "ESP-0412"
    assert escolhida.texto == "Café 250 g"
    assert sorted(escolhida.tolerancias) == ["cof", "espessura", "selagem"]
    assert escolhida.tolerancias["cof"].maximo == 0.25, "o cliente vence o padrão"
    assert escolhida.tolerancias["selagem"].minimo == 12.0, "o cliente vence o padrão"
    assert escolhida.tolerancias["espessura"].percentual == 8.0, "o resto vem do padrão C"


@pytest.mark.parametrize("titulo", [" esp-0412 ", "Esp-0412", "ESP-0412\t"])
def test_titulo_sem_diferenciar_maiusculas_e_espacos(especificacoes, titulo):
    assert ex.escolher_especificacao(titulo, "A", especificacoes).titulo == "ESP-0412"


def test_nao_altera_os_originais(especificacoes):
    ex.escolher_especificacao("ESP-0412", "C", especificacoes)
    assert especificacoes["PADRAO-C"].tolerancias["cof"].maximo == 0.30
    assert sorted(especificacoes["ESP-0412"].tolerancias) == ["cof", "selagem"]


def test_titulo_desconhecido_nunca_vira_padrao(especificacoes):
    with pytest.raises(ex.EspecificacaoDesconhecida) as erro:
        ex.escolher_especificacao(" ESP-9999 ", "A", especificacoes)
    assert str(erro.value) == "especificação 'ESP-9999' não cadastrada"


def test_linha_sem_padrao(especificacoes):
    with pytest.raises(ex.EspecificacaoDesconhecida) as erro:
        ex.escolher_especificacao("", "B", especificacoes)
    assert str(erro.value) == "linha B sem especificação padrão cadastrada"


@pytest.mark.parametrize(
    ("titulo", "esperado"),
    [("  esp-0412 ", "ESP-0412"), ("Esp  Cliente   X", "ESP CLIENTE X"), ("", "")],
)
def test_chave_titulo(titulo, esperado):
    assert ex.chave_titulo(titulo) == esperado
