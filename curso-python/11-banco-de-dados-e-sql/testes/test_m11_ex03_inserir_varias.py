import sqlite3

import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_inserir_varias")

SQL = """
CREATE TABLE ensaio (
    id INTEGER PRIMARY KEY, op INTEGER NOT NULL, bobina INTEGER NOT NULL,
    caracteristica TEXT NOT NULL, valor REAL)
"""


@pytest.fixture
def conexao():
    con = sqlite3.connect(":memory:")
    con.execute(SQL)
    yield con
    con.close()


def total(con):
    return con.execute("SELECT COUNT(*) FROM ensaio").fetchone()[0]


def test_insere_e_devolve_a_quantidade(conexao):
    lote = [(24518, 1, "espessura", 38.8), (24518, 1, "cof", 0.31), (24518, 2, "cof", None)]
    assert ex.inserir_ensaios(conexao, lote) == 3
    assert total(conexao) == 3
    linhas = conexao.execute(
        "SELECT op, bobina, caracteristica, valor FROM ensaio ORDER BY id"
    )
    assert linhas.fetchall() == lote


def test_lista_vazia_devolve_zero(conexao):
    assert ex.inserir_ensaios(conexao, []) == 0
    assert total(conexao) == 0


def test_lote_com_erro_nao_grava_nada(conexao):
    lote = [(24518, 1, "espessura", 38.8), (24518, 1, None, 0.31), (24518, 2, "cof", 0.2)]
    with pytest.raises(sqlite3.IntegrityError):
        ex.inserir_ensaios(conexao, lote)
    assert total(conexao) == 0, "transação: se uma linha falha, nenhuma pode ficar gravada"


def test_faz_commit(conexao):
    ex.inserir_ensaios(conexao, [(24518, 1, "espessura", 38.8)])
    assert not conexao.in_transaction, "use 'with conexao:' (ou commit) para gravar"
