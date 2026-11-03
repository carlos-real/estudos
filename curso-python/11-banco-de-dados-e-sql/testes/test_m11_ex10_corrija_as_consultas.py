import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_corrija_as_consultas")

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


def test_ensaios_sem_valor(conexao):
    assert ex.ensaios_sem_valor(conexao) == [(24534, 2, "cof")], "NULL se testa com IS NULL"


def test_ensaios_por_op_conta_zero_para_quem_nao_tem(conexao):
    resultado = dict(ex.ensaios_por_op(conexao))
    assert resultado[24550] == 0, "COUNT(*) conta a linha 'vazia' do LEFT JOIN"
    assert resultado[24551] == 0
    assert resultado[24518] == 6


def test_ensaios_por_op_tem_todas_as_ops_em_ordem(conexao):
    numeros = [numero for numero, _ in ex.ensaios_por_op(conexao)]
    assert numeros == sorted(numeros) and len(numeros) == 12


def test_clientes_e_ops_da_linha_b(conexao):
    assert ex.clientes_e_ops_da_linha(conexao, "B") == [
        ("Agro Campo S.A.", None),
        ("Biscoitos Aurora", None),
        ("Café do Vale", None),
        ("Higiene Bem-Estar S.A.", 24528),
        ("Higiene Bem-Estar S.A.", 24550),
        ("Laticínios Serra Azul", 24527),
        ("Torrefação Serra Ltda", None),
    ]


def test_clientes_e_ops_de_linha_sem_ops(conexao):
    resultado = ex.clientes_e_ops_da_linha(conexao, "X")
    assert len(resultado) == 6, "todos os clientes aparecem, mesmo sem OP na linha"
    assert all(numero is None for _, numero in resultado)
