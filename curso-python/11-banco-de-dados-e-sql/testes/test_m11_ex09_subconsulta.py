import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_subconsulta")

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


def test_ops_acima_da_media(conexao):
    assert ex.ops_acima_da_media(conexao) == [
        (24521, 6000.0), (24520, 5200.0), (24518, 4500.0), (24551, 4100.0), (24541, 4000.0),
        (24546, 3800.0),
    ]  # fmt: skip


def test_media_muda_com_os_dados(conexao):
    conexao.execute("UPDATE op SET quantidade_kg = 100000 WHERE numero = 24550")
    assert ex.ops_acima_da_media(conexao) == [(24550, 100000.0)]


def test_ops_com_reprovacao(conexao):
    assert ex.ops_com_reprovacao(conexao) == [24519, 24527, 24533, 24546]


def test_ops_com_reprovacao_sem_repetir(conexao):
    resultado = ex.ops_com_reprovacao(conexao)
    assert len(resultado) == len(set(resultado)), "a OP 24533 tem 2 FORA: deve aparecer 1 vez"


def test_clientes_sem_op(conexao):
    assert ex.clientes_sem_op(conexao) == ["Café do Vale"]


def test_clientes_sem_op_com_cliente_novo(conexao):
    conexao.execute("INSERT INTO cliente (nome) VALUES ('Açúcar Doce Vida')")
    assert ex.clientes_sem_op(conexao) == ["Açúcar Doce Vida", "Café do Vale"]
