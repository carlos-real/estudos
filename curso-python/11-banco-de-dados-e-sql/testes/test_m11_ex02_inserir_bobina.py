import sqlite3

import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_inserir_bobina")

SQL = """
CREATE TABLE bobina (
    id INTEGER PRIMARY KEY, op INTEGER NOT NULL, numero INTEGER NOT NULL,
    peso_kg REAL NOT NULL CHECK (peso_kg > 0), UNIQUE (op, numero))
"""


@pytest.fixture
def caminho(tmp_path):
    caminho = tmp_path / "bobinas.db"
    con = sqlite3.connect(caminho)
    con.execute(SQL)
    con.commit()
    con.close()
    return caminho


@pytest.fixture
def conexao(caminho):
    con = sqlite3.connect(caminho)
    yield con
    con.close()


def test_devolve_os_ids_gerados(conexao):
    assert ex.inserir_bobina(conexao, 24518, 1, 1250.5) == 1
    assert ex.inserir_bobina(conexao, 24518, 2, 980.0) == 2


def test_grava_os_valores(conexao):
    ex.inserir_bobina(conexao, 24541, 3, 2000.25)
    linha = conexao.execute("SELECT op, numero, peso_kg FROM bobina").fetchone()
    assert linha == (24541, 3, 2000.25)


def test_faz_commit(conexao, caminho):
    ex.inserir_bobina(conexao, 24518, 1, 1250.5)
    outra = sqlite3.connect(caminho)  # outro "programa" abrindo o mesmo arquivo
    try:
        total = outra.execute("SELECT COUNT(*) FROM bobina").fetchone()[0]
    finally:
        outra.close()
    assert total == 1, "faltou conexao.commit(): outra conexão não enxerga a bobina"


@pytest.mark.parametrize("peso", [0, -10.5])
def test_peso_invalido_levanta_integrity_error(conexao, peso):
    with pytest.raises(sqlite3.IntegrityError):
        ex.inserir_bobina(conexao, 24518, 1, peso)


def test_bobina_repetida_levanta_integrity_error(conexao):
    ex.inserir_bobina(conexao, 24518, 1, 1250.5)
    with pytest.raises(sqlite3.IntegrityError):
        ex.inserir_bobina(conexao, 24518, 1, 999.0)


def test_contar_bobinas(conexao):
    for numero, peso in [(1, 1250.5), (2, 980.0), (3, 1100.0)]:
        conexao.execute(
            "INSERT INTO bobina (op, numero, peso_kg) VALUES (?, ?, ?)", (24518, numero, peso)
        )
    conexao.execute("INSERT INTO bobina (op, numero, peso_kg) VALUES (24519, 1, 500)")
    assert ex.contar_bobinas(conexao, 24518) == 3
    assert ex.contar_bobinas(conexao, 24519) == 1
    assert ex.contar_bobinas(conexao, 99999) == 0
