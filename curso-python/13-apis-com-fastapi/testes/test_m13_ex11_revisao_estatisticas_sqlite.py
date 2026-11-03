import sqlite3

import pytest
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex11_revisao_estatisticas_sqlite")

ESQUEMA = """CREATE TABLE medicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, op TEXT NOT NULL,
    ensaio TEXT NOT NULL, valor REAL NOT NULL)"""


@pytest.fixture(autouse=True)
def limpar_overrides():
    yield
    ex.app.dependency_overrides.clear()


def cliente_com_banco():
    """Banco em memória no lugar do arquivo: cada teste começa do zero."""
    con = sqlite3.connect(":memory:", check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute(ESQUEMA)
    ex.app.dependency_overrides[ex.obter_conexao] = lambda: con
    return TestClient(ex.app), con


def lancar(cliente, op, ensaio, valor):
    resposta = cliente.post("/medicoes", json={"op": op, "ensaio": ensaio, "valor": valor})
    assert resposta.status_code == 201, f"POST /medicoes deveria dar 201, deu {resposta.status_code}"
    return resposta.json()


def test_criar_tabela(tmp_path):
    con = sqlite3.connect(tmp_path / "t.db")
    ex.criar_tabela(con)
    ex.criar_tabela(con)  # segunda vez não pode dar erro (IF NOT EXISTS)
    colunas = [linha[1] for linha in con.execute("PRAGMA table_info(medicoes)")]
    assert colunas == ["id", "op", "ensaio", "valor"]
    con.close()


def test_obter_conexao_entrega_e_fecha(tmp_path, monkeypatch):
    monkeypatch.setattr(ex, "CAMINHO_BANCO", tmp_path / "lab.db")
    gerador = ex.obter_conexao()
    con = next(gerador)
    assert con.row_factory is sqlite3.Row
    con.execute("INSERT INTO medicoes (op, ensaio, valor) VALUES ('123456', 'cof', 0.2)")
    gerador.close()  # simula o fim da requisição: o finally deve fechar a conexão
    with pytest.raises(sqlite3.ProgrammingError):
        con.execute("SELECT 1")
    assert (tmp_path / "lab.db").exists()


def test_post_grava_no_banco():
    cliente, con = cliente_com_banco()
    assert lancar(cliente, "123456", "cof", 0.25) == {
        "id": 1, "op": "123456", "ensaio": "cof", "valor": 0.25
    }
    assert lancar(cliente, "123456", "cof", 0.27)["id"] == 2
    assert con.execute("SELECT COUNT(*) FROM medicoes").fetchone()[0] == 2


@pytest.mark.parametrize(
    "corpo",
    [
        {"op": "12345", "ensaio": "cof", "valor": 0.2},
        {"op": "123456", "ensaio": "c", "valor": 0.2},
        {"op": "123456", "ensaio": "cof", "valor": 0},
        {"op": "123456", "ensaio": "cof"},
    ],
)
def test_post_invalido_da_422(corpo):
    cliente, _ = cliente_com_banco()
    lancar(cliente, "123456", "cof", 0.25)
    assert cliente.post("/medicoes", json=corpo).status_code == 422


def test_resumo_estatistico():
    cliente, _ = cliente_com_banco()
    for valor in [20.1, 20.4, 19.8]:
        lancar(cliente, "123456", "espessura", valor)
    lancar(cliente, "123456", "cof", 0.25)
    lancar(cliente, "999999", "espessura", 50.0)  # outra OP: não entra

    resposta = cliente.get("/ops/123456/resumo")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["op"] == "123456"
    assert list(dados["ensaios"]) == ["cof", "espessura"], "Ensaios em ordem alfabética"
    assert dados["ensaios"]["cof"] == {
        "n": 1, "media": 0.25, "desvio": 0.0, "minimo": 0.25, "maximo": 0.25
    }
    espessura = dados["ensaios"]["espessura"]
    assert espessura["n"] == 3
    assert espessura["media"] == pytest.approx(20.1)
    assert espessura["desvio"] == pytest.approx(0.3)
    assert (espessura["minimo"], espessura["maximo"]) == (19.8, 20.4)


def test_media_e_desvio_arredondados():
    cliente, _ = cliente_com_banco()
    for valor in [1.0, 2.0, 2.0]:
        lancar(cliente, "124001", "tracao", valor)
    tracao = cliente.get("/ops/124001/resumo").json()["ensaios"]["tracao"]
    assert tracao["media"] == 1.667
    assert tracao["desvio"] == 0.577


def test_op_sem_medicoes_da_404():
    cliente, _ = cliente_com_banco()
    lancar(cliente, "123456", "cof", 0.25)
    resposta = cliente.get("/ops/654321/resumo")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "OP 654321 sem medições"}
