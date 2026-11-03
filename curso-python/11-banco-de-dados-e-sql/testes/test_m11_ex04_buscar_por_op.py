import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_buscar_por_op")

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


def test_ensaios_da_op_ordenados(conexao):
    assert ex.ensaios_da_op(conexao, 24534) == [
        (1, "cof", 0.23),
        (1, "espessura", 69.8),
        (1, "gramatura", 65.6),
        (2, "cof", None),
        (2, "espessura", 67.3),
        (2, "gramatura", 66.8),
    ]


def test_op_sem_ensaios_devolve_lista_vazia(conexao):
    assert ex.ensaios_da_op(conexao, 24550) == []
    assert ex.ensaios_da_op(conexao, 99999) == []


def test_ensaios_de_outra_op(conexao):
    resultado = ex.ensaios_da_op(conexao, 24527)
    assert len(resultado) == 6
    assert (1, "cof", 0.43) in resultado


@pytest.mark.parametrize(
    ("numero", "esperado"), [(24534, True), (24551, True), (99999, False)]
)
def test_existe_op(conexao, numero, esperado):
    assert ex.existe_op(conexao, numero) is esperado
