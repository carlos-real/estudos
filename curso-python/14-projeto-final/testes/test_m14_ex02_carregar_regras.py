import sqlite3

import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_carregar_regras")


@pytest.fixture
def conexao():
    """Banco em memória com o schema do exercício e dados pequenos."""
    conexao = sqlite3.connect(":memory:")
    conexao.executescript(ex.SCHEMA)
    conexao.executemany("INSERT INTO linha VALUES (?, ?)", [("A", "Extrusora 1")])
    conexao.executemany(
        "INSERT INTO especificacao VALUES (?, ?, ?)",
        [
            ("PADRAO-A", "Padrão da linha A", "A"),
            ("ESP-0412", "Café 250 g", None),
            ("ESP-0700", "Ainda sem tolerâncias", None),
        ],
    )
    conexao.executemany(
        "INSERT INTO tolerancia VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("PADRAO-A", "espessura", "nominal", None, None, 10.0),
            ("PADRAO-A", "cof", "fixa", 0.15, 0.35, None),
            ("PADRAO-A", "selagem", "fixa", 8.0, None, None),
            ("ESP-0412", "cof", "fixa", 0.18, 0.25, None),
        ],
    )
    yield conexao
    conexao.close()


def test_devolve_todas_as_especificacoes(conexao):
    especificacoes = ex.carregar_especificacoes(conexao)
    assert sorted(especificacoes) == ["ESP-0412", "ESP-0700", "PADRAO-A"]
    assert all(isinstance(e, ex.Especificacao) for e in especificacoes.values())


def test_linha_e_texto(conexao):
    especificacoes = ex.carregar_especificacoes(conexao)
    assert especificacoes["PADRAO-A"].linha == "A"
    assert especificacoes["ESP-0412"].linha == "", "NULL no banco deve virar '' no objeto"
    assert especificacoes["ESP-0412"].texto == "Café 250 g"


def test_tolerancias_do_padrao(conexao):
    padrao = ex.carregar_especificacoes(conexao)["PADRAO-A"]
    assert sorted(padrao.tolerancias) == ["cof", "espessura", "selagem"]
    assert padrao.tolerancias["espessura"] == ex.Tolerancia(
        "espessura", "nominal", percentual=10.0
    )
    assert padrao.tolerancias["selagem"] == ex.Tolerancia("selagem", "fixa", minimo=8.0)


def test_tolerancias_nao_se_misturam_entre_especificacoes(conexao):
    especificacoes = ex.carregar_especificacoes(conexao)
    assert list(especificacoes["ESP-0412"].tolerancias) == ["cof"]
    assert especificacoes["ESP-0412"].tolerancias["cof"].maximo == 0.25
    assert especificacoes["ESP-0700"].tolerancias == {}


def test_banco_vazio_devolve_dicionario_vazio():
    conexao = sqlite3.connect(":memory:")
    conexao.executescript(ex.SCHEMA)
    assert ex.carregar_especificacoes(conexao) == {}
    conexao.close()


def test_nao_fecha_a_conexao(conexao):
    ex.carregar_especificacoes(conexao)
    assert conexao.execute("SELECT COUNT(*) FROM especificacao").fetchone() == (3,)


def test_regra_quebrada_no_banco_levanta_value_error(conexao):
    conexao.execute(
        "INSERT INTO tolerancia VALUES ('ESP-0700', 'cof', 'fixa', NULL, NULL, NULL)"
    )
    with pytest.raises(ValueError):
        ex.carregar_especificacoes(conexao)
