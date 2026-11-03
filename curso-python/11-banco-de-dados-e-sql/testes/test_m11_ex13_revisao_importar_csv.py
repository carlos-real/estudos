import sqlite3
from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_importar_csv")

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


CABECALHO = "op;nf;peso;data\n"


def criar_csv(pasta, linhas):
    caminho = pasta / "expedicao.csv"
    caminho.write_text(
        CABECALHO + "".join(linha + "\n" for linha in linhas), encoding="utf-8-sig"
    )
    return caminho


def novas(con):
    return con.execute(
        "SELECT op, nf, peso_kg, data FROM expedicao WHERE id > 8 ORDER BY id"
    ).fetchall()


def test_importa_linhas_validas(conexao, tmp_path):
    caminho = criar_csv(
        tmp_path, ["24518;123480;1.250,5;30/10/2026", "24541;000123;980;31/10/2026"]
    )
    assert ex.importar_expedicao(conexao, caminho) == (2, [])
    assert novas(conexao) == [
        (24518, "123480", 1250.5, "2026-10-30"),
        (24541, "000123", 980.0, "2026-10-31"),
    ], "NF é texto (zeros à esquerda) e a data vai no formato AAAA-MM-DD"


def test_linhas_invalidas_vao_para_a_lista_de_erros(conexao, tmp_path):
    caminho = criar_csv(
        tmp_path,
        [
            "24518;123480;1.250,5;30/10/2026",  # linha 2: ok
            "99999;123481;100,0;30/10/2026",  # linha 3: OP não existe
            "24518;123482;0,0;30/10/2026",  # linha 4: peso zero
            "24518;123483;abc;30/10/2026",  # linha 5: peso inválido
            "24518;123484;10,0;31/09/2026",  # linha 6: data inexistente
            "24518;;10,0;30/10/2026",  # linha 7: NF vazia
            "OP24518;123485;10,0;30/10/2026",  # linha 8: OP não numérica
            "24520;123486;2.400,0;01/11/2026",  # linha 9: ok
        ],
    )
    assert ex.importar_expedicao(conexao, caminho) == (2, [3, 4, 5, 6, 7, 8])
    assert [nf for _, nf, _, _ in novas(conexao)] == ["123480", "123486"]


def test_arquivo_so_com_cabecalho(conexao, tmp_path):
    caminho = criar_csv(tmp_path, [])
    assert ex.importar_expedicao(conexao, caminho) == (0, [])
    assert novas(conexao) == []


def test_grava_com_commit(conexao, tmp_path):
    caminho = criar_csv(tmp_path, ["24518;123480;1.250,5;30/10/2026"])
    ex.importar_expedicao(conexao, caminho)
    assert not conexao.in_transaction, "use 'with conexao:' (ou commit) para gravar"
