import pytest
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex06_validar_medicao")
cliente = TestClient(ex.app)


@pytest.mark.parametrize(
    ("valor", "minimo", "maximo", "esperado"),
    [
        (20.4, 18.0, 22.0, (True, 1.6)),
        (18.0, 18.0, 22.0, (True, 0.0)),
        (22.0, 18.0, 22.0, (True, 0.0)),
        (23.0, 18.0, 22.0, (False, -1.0)),
        (0.31, 0.2, 0.3, (False, -0.01)),
    ],
)
def test_avaliar(valor, minimo, maximo, esperado):
    aprovado, margem = ex.avaliar(valor, minimo, maximo)
    assert aprovado is esperado[0]
    assert margem == pytest.approx(esperado[1])


def test_medicao_aprovada():
    resposta = cliente.post("/validar", json={"linha": "A", "ensaio": "espessura", "valor": 20.4})
    assert resposta.status_code == 200, "A rota POST /validar ainda não existe"
    assert resposta.json() == {
        "linha": "A",
        "ensaio": "espessura",
        "valor": 20.4,
        "minimo": 18.0,
        "maximo": 22.0,
        "margem": 1.6,
        "aprovado": True,
    }


def test_medicao_reprovada_e_padronizacao():
    resposta = cliente.post("/validar", json={"linha": "a", "ensaio": " COF ", "valor": 0.31})
    assert resposta.status_code == 200
    dados = resposta.json()
    assert (dados["linha"], dados["ensaio"]) == ("A", "cof")
    assert dados["aprovado"] is False
    assert dados["margem"] == pytest.approx(-0.01)


def test_resposta_tem_exatamente_os_campos_do_modelo():
    resposta = cliente.post("/validar", json={"linha": "C", "ensaio": "tracao", "valor": 30})
    assert resposta.status_code == 200
    assert set(resposta.json()) == {
        "linha", "ensaio", "valor", "minimo", "maximo", "margem", "aprovado"
    }


@pytest.mark.parametrize(
    ("corpo", "detalhe"),
    [
        ({"linha": "E", "ensaio": "cof", "valor": 1}, "linha E / ensaio cof"),
        ({"linha": "b", "ensaio": "COF", "valor": 1}, "linha B / ensaio cof"),
    ],
)
def test_sem_tolerancia_da_404(corpo, detalhe):
    ok = cliente.post("/validar", json={"linha": "B", "ensaio": "gramatura", "valor": 37})
    assert ok.status_code == 200, "A rota POST /validar ainda não existe"
    resposta = cliente.post("/validar", json=corpo)
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": f"Tolerância não cadastrada: {detalhe}"}


@pytest.mark.parametrize(
    "corpo",
    [
        {"linha": "A", "ensaio": "cof", "valor": -0.1},
        {"linha": "A", "ensaio": "cof"},
        {"linha": "A", "valor": 0.25},
        {"linha": "A", "ensaio": "cof", "valor": "muito"},
    ],
)
def test_corpo_invalido_da_422(corpo):
    ok = cliente.post("/validar", json={"linha": "A", "ensaio": "cof", "valor": 0.25})
    assert ok.status_code == 200, "A rota POST /validar ainda não existe"
    assert cliente.post("/validar", json=corpo).status_code == 422
