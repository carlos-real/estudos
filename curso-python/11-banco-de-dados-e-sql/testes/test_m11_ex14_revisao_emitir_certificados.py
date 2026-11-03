import sqlite3
from datetime import date
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex14_revisao_emitir_certificados")

SQL_LAB = (Path(__file__).resolve().parent.parent / "dados" / "laboratorio.sql").read_text(
    encoding="utf-8"
)
SQL_CERTIFICADO = """
CREATE TABLE certificado (
    id           INTEGER PRIMARY KEY,
    numero       TEXT NOT NULL UNIQUE,
    expedicao_id INTEGER NOT NULL UNIQUE REFERENCES expedicao (id),
    emitido_em   TEXT NOT NULL
);
"""


@pytest.fixture
def conexao():
    con = sqlite3.connect(":memory:")
    con.executescript(SQL_LAB + SQL_CERTIFICADO)
    yield con
    con.close()


def gravados(con):
    return con.execute("SELECT numero, expedicao_id, emitido_em FROM certificado ORDER BY id")


def test_emite_para_as_cargas_elegiveis(conexao):
    emitidos = ex.emitir_certificados(conexao, date(2026, 10, 30))
    assert [(c.numero, c.op, c.nf) for c in emitidos] == [
        ("CQ-2026-0001", 24518, "123456"),
        ("CQ-2026-0002", 24518, "123470"),
        ("CQ-2026-0003", 24520, "123458"),
        ("CQ-2026-0004", 24521, "123459"),
        ("CQ-2026-0005", 24541, "123465"),
        ("CQ-2026-0006", 24541, "123466"),
    ], "só OPs LIBERADAS, sem FORA e sem ensaio pendente; ordem de expedicao.id"


def test_devolve_objetos_certificado_completos(conexao):
    primeiro = ex.emitir_certificados(conexao, date(2026, 10, 30))[0]
    assert primeiro == ex.Certificado("CQ-2026-0001", 24518, "123456", 1250.5, "2026-10-30")


def test_grava_no_banco(conexao):
    ex.emitir_certificados(conexao, date(2026, 10, 30))
    linhas = gravados(conexao).fetchall()
    assert [(n, e) for n, e, _ in linhas] == [
        ("CQ-2026-0001", 1), ("CQ-2026-0002", 2), ("CQ-2026-0003", 3), ("CQ-2026-0004", 4),
        ("CQ-2026-0005", 7), ("CQ-2026-0006", 8),
    ]  # fmt: skip
    assert {data for *_, data in linhas} == {"2026-10-30"}
    assert not conexao.in_transaction, "faltou gravar (with conexao: ou commit)"


def test_segunda_chamada_nao_emite_nada(conexao):
    ex.emitir_certificados(conexao, date(2026, 10, 30))
    assert ex.emitir_certificados(conexao, date(2026, 10, 31)) == []


def test_ignora_op_com_ensaio_pendente_ou_sem_ensaio(conexao):
    conexao.execute("UPDATE op SET status = 'LIBERADA' WHERE numero IN (24534, 24550)")
    conexao.executemany(
        "INSERT INTO expedicao (op, nf, peso_kg, data) VALUES (?, ?, ?, '2026-10-30')",
        [(24534, "200001", 100.0), (24550, "200002", 100.0)],
    )
    ops = {c.op for c in ex.emitir_certificados(conexao, date(2026, 10, 30))}
    assert 24534 not in ops, "a OP 24534 tem ensaio sem valor"
    assert 24550 not in ops, "a OP 24550 não tem nenhum ensaio"


def test_sequencia_continua_do_maior_numero_do_ano(conexao):
    conexao.execute(
        "INSERT INTO certificado (numero, expedicao_id, emitido_em) "
        "VALUES ('CQ-2026-0041', 5, '2026-10-25')"
    )
    emitidos = ex.emitir_certificados(conexao, date(2026, 10, 30))
    assert emitidos[0].numero == "CQ-2026-0042"
    assert emitidos[-1].numero == "CQ-2026-0047"


def test_ano_novo_recomeca_a_sequencia(conexao):
    conexao.execute(
        "INSERT INTO certificado (numero, expedicao_id, emitido_em) "
        "VALUES ('CQ-2026-0041', 5, '2026-10-25')"
    )
    emitidos = ex.emitir_certificados(conexao, date(2027, 1, 4))
    assert emitidos[0].numero == "CQ-2027-0001"
    assert emitidos[0].emitido_em == "2027-01-04"


def test_erro_no_meio_desfaz_tudo(conexao):
    conexao.execute(
        "CREATE TRIGGER falha BEFORE INSERT ON certificado WHEN NEW.expedicao_id = 4 "
        "BEGIN SELECT RAISE(ABORT, 'falha simulada'); END"
    )
    with pytest.raises(sqlite3.IntegrityError):
        ex.emitir_certificados(conexao, date(2026, 10, 30))
    assert gravados(conexao).fetchall() == [], "transação: nada pode ficar gravado"
