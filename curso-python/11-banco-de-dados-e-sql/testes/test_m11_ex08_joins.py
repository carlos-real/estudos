import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_joins")

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


def test_relatorio_ops_da_linha_d(conexao):
    assert ex.relatorio_ops(conexao, "D") == [
        {
            "numero": 24541,
            "cliente": "Torrefação Serra Ltda",
            "produto": "Laminado PET/PE 62 µm",
        },
        {
            "numero": 24546,
            "cliente": "Laticínios Serra Azul",
            "produto": "Laminado BOPP/PE 55 µm",
        },
        {"numero": 24551, "cliente": "Agro Campo S.A.", "produto": "Laminado PET/PE 62 µm"},
    ]


def test_relatorio_de_linha_sem_ops(conexao):
    conexao.execute("INSERT INTO linha VALUES ('E', 'Linha nova')")
    assert ex.relatorio_ops(conexao, "E") == []


def test_ops_sem_ensaio(conexao):
    assert ex.ops_sem_ensaio(conexao) == [24550, 24551]


def test_ops_sem_ensaio_depois_de_medir(conexao):
    conexao.execute(
        "INSERT INTO ensaio (op, bobina, caracteristica, valor, data) "
        "VALUES (24550, 1, 'cof', 0.3, '2026-10-27')"
    )
    assert ex.ops_sem_ensaio(conexao) == [24551]


def test_peso_por_cliente_inclui_quem_nao_expediu(conexao):
    resultado = ex.peso_por_cliente(conexao)
    assert [nome for nome, _ in resultado] == [
        "Torrefação Serra Ltda",
        "Agro Campo S.A.",
        "Higiene Bem-Estar S.A.",
        "Biscoitos Aurora",
        "Café do Vale",
        "Laticínios Serra Azul",
    ], "todos os 6 clientes, por peso decrescente e depois por nome"
    assert [peso for _, peso in resultado] == pytest.approx([6830.75, 5350.0, 2750.5, 0, 0, 0])
