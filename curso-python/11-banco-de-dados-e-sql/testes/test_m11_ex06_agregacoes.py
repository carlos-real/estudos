import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_agregacoes")

SQL_LAB = (Path(__file__).resolve().parent.parent / "dados" / "laboratorio.sql").read_text(
    encoding="utf-8"
)


@pytest.fixture
def conexao():
    """Banco do laboratório (dados/laboratorio.sql), na memória."""
    con = sqlite3.connect(":memory:")
    con.executescript(SQL_LAB)
    yield con
    con.close()


def test_resumo_do_cof_ignora_o_pendente(conexao):
    resumo = ex.resumo_caracteristica(conexao, "cof")
    assert resumo["n"] == 19, "são 20 ensaios de COF, mas 1 está sem valor (NULL)"
    assert resumo["media"] == pytest.approx(0.25)
    assert resumo["minimo"] == pytest.approx(0.15)
    assert resumo["maximo"] == pytest.approx(0.43)


def test_resumo_da_espessura(conexao):
    assert ex.resumo_caracteristica(conexao, "espessura") == {
        "n": 20,
        "media": pytest.approx(52.05),
        "minimo": pytest.approx(33.8),
        "maximo": pytest.approx(75.8),
    }


def test_caracteristica_sem_medicoes(conexao):
    assert ex.resumo_caracteristica(conexao, "selagem") == {
        "n": 0, "media": None, "minimo": None, "maximo": None
    }  # fmt: skip


@pytest.mark.parametrize(
    ("op", "esperado"),
    [(None, 14931.25), (24518, 3080.5), (24541, 3750.25), (24550, 0.0)],
)
def test_peso_expedido(conexao, op, esperado):
    resultado = ex.peso_expedido(conexao, op) if op else ex.peso_expedido(conexao)
    assert resultado == pytest.approx(esperado)
    assert isinstance(resultado, float), "devolva sempre float (0.0 quando não houver carga)"
