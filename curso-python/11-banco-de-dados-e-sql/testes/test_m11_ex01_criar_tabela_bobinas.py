import sqlite3

import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_criar_tabela_bobinas")


@pytest.fixture
def conexao():
    con = sqlite3.connect(":memory:")
    yield con
    con.close()


def inserir(con, op, numero, peso):
    con.execute("INSERT INTO bobina (op, numero, peso_kg) VALUES (?, ?, ?)", (op, numero, peso))


def test_tabela_existe(conexao):
    ex.criar_tabela_bobinas(conexao)
    nomes = [n for (n,) in conexao.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    assert "bobina" in nomes, "a tabela deve se chamar 'bobina'"


def test_colunas_na_ordem_e_com_tipos(conexao):
    ex.criar_tabela_bobinas(conexao)
    colunas = [(c[1], c[2].upper()) for c in conexao.execute("PRAGMA table_info(bobina)")]
    assert colunas == [
        ("id", "INTEGER"), ("op", "INTEGER"), ("numero", "INTEGER"), ("peso_kg", "REAL")
    ]  # fmt: skip


def test_id_e_numerado_sozinho(conexao):
    ex.criar_tabela_bobinas(conexao)
    inserir(conexao, 24518, 1, 1250.5)
    inserir(conexao, 24518, 2, 980.0)
    assert [i for (i,) in conexao.execute("SELECT id FROM bobina ORDER BY id")] == [1, 2]


@pytest.mark.parametrize(
    ("op", "numero", "peso"),
    [(None, 1, 100.0), (24518, None, 100.0), (24518, 1, None), (24518, 1, 0), (24518, 1, -5)],
)
def test_restricoes_recusam_dados_invalidos(conexao, op, numero, peso):
    ex.criar_tabela_bobinas(conexao)
    with pytest.raises(sqlite3.IntegrityError):
        inserir(conexao, op, numero, peso)


def test_op_e_numero_repetidos_sao_recusados(conexao):
    ex.criar_tabela_bobinas(conexao)
    inserir(conexao, 24518, 1, 1250.5)
    inserir(conexao, 24519, 1, 900.0)  # mesmo número, outra OP: pode
    with pytest.raises(sqlite3.IntegrityError):
        inserir(conexao, 24518, 1, 980.0)


def test_chamar_duas_vezes_nao_da_erro(conexao):
    ex.criar_tabela_bobinas(conexao)
    inserir(conexao, 24518, 1, 1250.5)
    conexao.commit()
    ex.criar_tabela_bobinas(conexao)  # IF NOT EXISTS
    assert conexao.execute("SELECT COUNT(*) FROM bobina").fetchone()[0] == 1
