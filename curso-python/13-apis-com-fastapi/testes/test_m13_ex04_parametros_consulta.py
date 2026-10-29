import pytest
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex04_parametros_consulta")
cliente = TestClient(ex.app)


def numeros(resposta):
    assert resposta.status_code == 200, f"Esperava 200, veio {resposta.status_code}"
    return [b["numero"] for b in resposta.json()]


def test_sem_filtros_devolve_as_10_primeiras():
    assert numeros(cliente.get("/bobinas")) == list(range(1, 11))


def test_filtra_por_linha_sem_diferenciar_maiusculas():
    assert numeros(cliente.get("/bobinas", params={"linha": "c"})) == [7, 8]
    assert numeros(cliente.get("/bobinas", params={"linha": "B"})) == [4, 5, 6]


def test_filtra_por_status():
    assert numeros(cliente.get("/bobinas", params={"status": "retida"})) == [3, 6, 8, 12]


def test_filtros_combinados():
    params = {"linha": "D", "status": "liberada", "peso_min": 800}
    assert numeros(cliente.get("/bobinas", params=params)) == [9, 11]


def test_peso_minimo_inclui_o_limite():
    assert numeros(cliente.get("/bobinas", params={"peso_min": 1100})) == [7, 8]


def test_limite():
    assert numeros(cliente.get("/bobinas", params={"limite": 3})) == [1, 2, 3]
    assert numeros(cliente.get("/bobinas", params={"limite": 50})) == list(range(1, 13))


def test_nenhuma_bobina_devolve_lista_vazia():
    assert numeros(cliente.get("/bobinas", params={"linha": "Z"})) == []


@pytest.mark.parametrize(
    "params", [{"limite": 0}, {"limite": 51}, {"limite": "abc"}, {"peso_min": -1}]
)
def test_valores_invalidos_dao_422(params):
    assert cliente.get("/bobinas").status_code == 200, "A rota GET /bobinas ainda não existe"
    assert cliente.get("/bobinas", params=params).status_code == 422
