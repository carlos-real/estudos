import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_banco_de_regras")

SQL_REGRAS = (Path(__file__).resolve().parent.parent / "dados" / "regras.sql").read_text(
    encoding="utf-8"
)


@pytest.fixture
def conexao():
    """Banco de regras (dados/regras.sql), na memória."""
    con = sqlite3.connect(":memory:")
    con.executescript(SQL_REGRAS)
    yield con
    con.close()


@pytest.mark.parametrize("titulo", [None, "", "   "])
def test_sem_titulo_usa_o_padrao_da_linha(conexao, titulo):
    assert ex.especificacao_da_op(conexao, "A", titulo) == (
        "PADRAO-A",
        "Padrão da linha A (filmes PE monocamada).",
    )


def test_titulo_sem_diferenciar_maiusculas_e_espacos(conexao):
    titulo, texto = ex.especificacao_da_op(conexao, "A", "  esp-0533 ")
    assert titulo == "ESP-0533"
    assert texto.startswith("Agro Campo")


@pytest.mark.parametrize(("linha", "titulo"), [("A", "ESP-9999"), ("E", None)])
def test_especificacao_inexistente_da_lookup_error(conexao, linha, titulo):
    with pytest.raises(LookupError):
        ex.especificacao_da_op(conexao, linha, titulo)


def test_tolerancias_do_padrao(conexao):
    efetivas = ex.tolerancias_efetivas(conexao, "D")
    assert set(efetivas) == {"espessura", "gramatura", "cof", "tracao", "selagem"}
    assert efetivas["cof"] == {
        "tipo": "fixa",
        "minimo": 0.15,
        "maximo": 0.30,
        "percentual": None,
        "origem": "PADRAO-D",
    }
    assert efetivas["espessura"]["percentual"] == 7.0


def test_especificacao_do_cliente_sobrescreve_o_padrao(conexao):
    efetivas = ex.tolerancias_efetivas(conexao, "A", "ESP-0533")
    assert efetivas["espessura"] == {
        "tipo": "nominal",
        "minimo": None,
        "maximo": None,
        "percentual": 5.0,
        "origem": "ESP-0533",
    }
    assert efetivas["tracao"]["minimo"] == 28.0
    assert efetivas["tracao"]["origem"] == "ESP-0533"
    assert efetivas["cof"]["origem"] == "PADRAO-A", "o que o cliente não define vem do padrão"
    assert len(efetivas) == 5


def test_tolerancias_com_titulo_desconhecido(conexao):
    with pytest.raises(LookupError):
        ex.tolerancias_efetivas(conexao, "A", "ESP-9999")


def test_limites_fixa():
    tol = {"tipo": "fixa", "minimo": 0.18, "maximo": 0.25, "percentual": None}
    assert ex.limites(tol) == (0.18, 0.25)
    so_minimo = {"tipo": "fixa", "minimo": 28.0, "maximo": None, "percentual": None}
    assert ex.limites(so_minimo) == (28.0, None)


@pytest.mark.parametrize(
    ("nominal", "percentual", "esperado"),
    [(60, 5.0, (57.0, 63.0)), (62, 7.0, (57.66, 66.34)), (46.3, 10.0, (41.67, 50.93))],
)
def test_limites_nominal(nominal, percentual, esperado):
    tol = {"tipo": "nominal", "minimo": None, "maximo": None, "percentual": percentual}
    assert ex.limites(tol, nominal) == pytest.approx(esperado)


@pytest.mark.parametrize("nominal", [None, 0, -10])
def test_limites_nominal_sem_nominal_valido(nominal):
    tol = {"tipo": "nominal", "minimo": None, "maximo": None, "percentual": 10.0}
    with pytest.raises(ValueError):
        ex.limites(tol, nominal)
