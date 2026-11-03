import pytest
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex07_ocorrencias")
cliente = TestClient(ex.app)

BOLHAS = {"op": "123456", "descricao": "Bolhas no filme", "gravidade": "alta"}
COF = {"op": "123789", "descricao": "COF acima do especificado", "gravidade": "media"}


@pytest.fixture(autouse=True)
def banco_vazio():
    ex.OCORRENCIAS.clear()
    yield
    ex.OCORRENCIAS.clear()


def criar(corpo):
    resposta = cliente.post("/ocorrencias", json=corpo)
    assert resposta.status_code == 201, (
        f"POST /ocorrencias deveria dar 201, deu {resposta.status_code}"
    )
    return resposta.json()


def test_criar_devolve_201_com_id_e_status():
    assert criar(BOLHAS) == {"id": 1, **BOLHAS, "status": "aberta"}
    assert criar(COF)["id"] == 2


def test_id_novo_e_o_maior_mais_um():
    criar(BOLHAS)
    criar(COF)
    assert cliente.delete("/ocorrencias/1").status_code == 204
    assert criar({**BOLHAS, "descricao": "Gel no filme"})["id"] == 3


def test_repetida_da_409():
    criar(BOLHAS)
    resposta = cliente.post("/ocorrencias", json=BOLHAS)
    assert resposta.status_code == 409
    assert resposta.json() == {"detail": "Ocorrência repetida"}
    # Mesma descrição em outra OP não é repetição:
    assert criar({**BOLHAS, "op": "999999"})["id"] == 2


@pytest.mark.parametrize(
    "corpo",
    [
        {**BOLHAS, "op": "12345"},
        {**BOLHAS, "descricao": "ruim"},
        {**BOLHAS, "gravidade": "gravissima"},
        {"op": "123456", "descricao": "Bolhas no filme"},
    ],
)
def test_entrada_invalida_da_422(corpo):
    criar(COF)
    assert cliente.post("/ocorrencias", json=corpo).status_code == 422


def test_listar_e_filtrar_por_status():
    criar(BOLHAS)
    criar(COF)
    assert cliente.patch("/ocorrencias/2/encerrar").status_code == 200
    todas = cliente.get("/ocorrencias").json()
    assert [o["id"] for o in todas] == [1, 2]
    abertas = cliente.get("/ocorrencias", params={"status": "aberta"}).json()
    assert [o["id"] for o in abertas] == [1]
    encerradas = cliente.get("/ocorrencias", params={"status": "encerrada"}).json()
    assert [o["id"] for o in encerradas] == [2]


def test_ver_uma_e_404():
    criar(BOLHAS)
    assert cliente.get("/ocorrencias/1").json() == {"id": 1, **BOLHAS, "status": "aberta"}
    resposta = cliente.get("/ocorrencias/42")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Ocorrência não encontrada"}


def test_encerrar_duas_vezes_da_409():
    criar(BOLHAS)
    resposta = cliente.patch("/ocorrencias/1/encerrar")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "encerrada"
    assert cliente.get("/ocorrencias/1").json()["status"] == "encerrada", "Guarde a mudança!"
    segunda = cliente.patch("/ocorrencias/1/encerrar")
    assert segunda.status_code == 409
    assert segunda.json() == {"detail": "Ocorrência já encerrada"}
    assert cliente.patch("/ocorrencias/7/encerrar").status_code == 404


def test_apagar_204_sem_corpo_e_depois_404():
    criar(BOLHAS)
    resposta = cliente.delete("/ocorrencias/1")
    assert resposta.status_code == 204
    assert resposta.content == b"", "204 não tem corpo"
    assert cliente.get("/ocorrencias/1").status_code == 404
    assert cliente.delete("/ocorrencias/1").status_code == 404
