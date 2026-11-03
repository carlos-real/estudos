import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_group_by_having")

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


def test_fora_por_caracteristica(conexao):
    assert ex.fora_por_caracteristica(conexao) == [("espessura", 3), ("cof", 2), ("gramatura", 1)]


def test_empate_em_ordem_alfabetica(conexao):
    conexao.execute("UPDATE ensaio SET resultado = 'FORA' WHERE op = 24518 AND bobina = 1")
    # agora: espessura 4, cof 3, gramatura 2
    conexao.execute("UPDATE ensaio SET resultado = 'FORA' WHERE op = 24520 AND bobina = 1 "
                    "AND caracteristica = 'gramatura'")  # fmt: skip
    assert ex.fora_por_caracteristica(conexao) == [
        ("espessura", 4), ("cof", 3), ("gramatura", 3)
    ]  # fmt: skip


def test_sem_nenhum_fora_devolve_lista_vazia(conexao):
    conexao.execute("UPDATE ensaio SET resultado = 'OK'")
    assert ex.fora_por_caracteristica(conexao) == []


def test_ops_com_duas_ou_mais_cargas(conexao):
    resultado = ex.ops_com_varias_cargas(conexao, 2)
    assert [(op, cargas) for op, cargas, _ in resultado] == [(24518, 2), (24528, 2), (24541, 2)]
    assert [peso for *_, peso in resultado] == pytest.approx([3080.5, 2750.5, 3750.25])


@pytest.mark.parametrize(("minimo", "quantidade"), [(1, 5), (3, 0)])
def test_minimo_de_cargas(conexao, minimo, quantidade):
    assert len(ex.ops_com_varias_cargas(conexao, minimo)) == quantidade
