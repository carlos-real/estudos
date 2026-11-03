import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_filtros_where")

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


@pytest.mark.parametrize(
    ("linha", "inicio", "fim", "esperado"),
    [
        ("A", "2026-10-20", "2026-10-20", [24518, 24519]),
        ("A", "2026-10-21", "2026-10-31", [24520, 24521]),
        ("D", "2026-10-01", "2026-10-31", [24541, 24546, 24551]),
        ("B", "2026-11-01", "2026-11-30", []),
    ],
)
def test_ops_da_linha_no_periodo(conexao, linha, inicio, fim, esperado):
    assert ex.ops_da_linha_no_periodo(conexao, linha, inicio, fim) == esperado


def test_periodo_inclui_as_pontas(conexao):
    assert ex.ops_da_linha_no_periodo(conexao, "B", "2026-10-21", "2026-10-22") == [24527, 24528]


def test_ensaios_pendentes(conexao):
    assert ex.ensaios_pendentes(conexao) == [(24534, 2, "cof")]


def test_ensaios_pendentes_ordenados(conexao):
    conexao.execute(
        "INSERT INTO ensaio (op, bobina, caracteristica, valor, data) "
        "VALUES (24518, 2, 'tracao', NULL, '2026-10-21')"
    )
    assert ex.ensaios_pendentes(conexao) == [(24518, 2, "tracao"), (24534, 2, "cof")]


@pytest.mark.parametrize(
    ("trecho", "esperado"),
    [
        ("laminado", ["Laminado BOPP/PE 55 µm", "Laminado PET/PE 62 µm"]),
        ("PE 35", ["Filme PE 35 µm"]),
        ("Filme PE 4", ["Filme PE 40 µm transparente"]),
        ("vidro", []),
    ],
)
def test_buscar_produtos(conexao, trecho, esperado):
    assert ex.buscar_produtos(conexao, trecho) == esperado
