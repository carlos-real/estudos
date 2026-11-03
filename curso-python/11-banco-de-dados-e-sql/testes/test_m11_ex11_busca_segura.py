import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_busca_segura")

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


def test_filtros_combinados(conexao):
    assert ex.buscar_ops(conexao, {"linha": "A", "status": "LIBERADA"}) == [
        24518,
        24520,
        24521,
    ]


def test_sem_filtros_devolve_todas_em_ordem(conexao):
    resultado = ex.buscar_ops(conexao, {})
    assert len(resultado) == 12
    assert resultado == sorted(resultado)


def test_filtro_por_especificacao(conexao):
    assert ex.buscar_ops(conexao, {"especificacao": "ESP-0533"}) == [24521]


@pytest.mark.parametrize(
    ("ordem", "esperado"),
    [
        ("quantidade_kg", [24527, 24550, 24528]),
        ("emissao", [24527, 24528, 24550]),
        ("numero", [24527, 24528, 24550]),
    ],
)
def test_ordenacao(conexao, ordem, esperado):
    assert ex.buscar_ops(conexao, {"linha": "B"}, ordenar_por=ordem) == esperado


@pytest.mark.parametrize(
    "ataque",
    ["A' OR '1'='1", "A'; DROP TABLE op; --", "x' UNION SELECT id FROM cliente --"],
)
def test_injection_no_valor_nao_funciona(conexao, ataque):
    assert ex.buscar_ops(conexao, {"linha": ataque}) == [], "use parâmetros (?) nos valores"
    assert conexao.execute("SELECT COUNT(*) FROM op").fetchone()[0] == 12


def test_valor_com_apostrofo_funciona(conexao):
    conexao.execute(
        "INSERT INTO op VALUES (24560, 'A', 1, 'Filme D''Ávila', NULL, '2026-10-28', 100, "
        "'ABERTA')"
    )
    assert ex.buscar_ops(conexao, {"produto": "Filme D'Ávila"}) == [24560]


@pytest.mark.parametrize("coluna", ["cor", "linha = 'A' OR 1=1 --", "cliente_id"])
def test_coluna_de_filtro_nao_permitida(conexao, coluna):
    with pytest.raises(ValueError):
        ex.buscar_ops(conexao, {coluna: "A"})


@pytest.mark.parametrize("ordem", ["numero; DROP TABLE op", "produto", "numero DESC"])
def test_ordenacao_nao_permitida(conexao, ordem):
    with pytest.raises(ValueError):
        ex.buscar_ops(conexao, {}, ordenar_por=ordem)
    assert conexao.execute("SELECT COUNT(*) FROM op").fetchone()[0] == 12
