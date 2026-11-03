import copy

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex09_dependencias")
cliente = TestClient(ex.app)

ESCRITA = {"X-Chave": "lab-123"}
LEITURA = {"X-Chave": "bi-789"}
ORIGINAL = copy.deepcopy(ex.REGRAS)


@pytest.fixture(autouse=True)
def restaurar():
    yield
    ex.app.dependency_overrides.clear()
    ex.REGRAS.clear()
    ex.REGRAS.update(copy.deepcopy(ORIGINAL))


def test_perfil_atual_direto():
    assert ex.perfil_atual("lab-123") == "escrita"
    assert ex.perfil_atual("bi-789") == "leitura"
    with pytest.raises(HTTPException) as erro:
        ex.perfil_atual(None)
    assert erro.value.status_code == 401


def test_ler_com_chave_de_leitura():
    resposta = cliente.get("/regras/A", headers=LEITURA)
    assert resposta.status_code == 200, "A rota GET /regras/{linha} ainda não existe"
    assert resposta.json() == {
        "linha": "A",
        "regras": {"espessura": [18.0, 22.0], "cof": [0.2, 0.3]},
    }


@pytest.mark.parametrize("cabecalhos", [{}, {"X-Chave": "senha123"}, {"X-Chave": ""}])
def test_sem_chave_valida_da_401(cabecalhos):
    assert cliente.get("/regras/B", headers=ESCRITA).status_code == 200
    resposta = cliente.get("/regras/B", headers=cabecalhos)
    assert resposta.status_code == 401
    assert resposta.json() == {"detail": "Chave de acesso inválida ou ausente"}


def test_linha_sem_regras_da_404():
    assert cliente.get("/regras/A", headers=ESCRITA).status_code == 200
    resposta = cliente.get("/regras/D", headers=ESCRITA)
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Linha D sem regras"}


def test_gravar_com_perfil_de_escrita():
    resposta = cliente.put(
        "/regras/D/selagem", json={"minimo": 1.5, "maximo": 3.0}, headers=ESCRITA
    )
    assert resposta.status_code == 200, "A rota PUT /regras/{linha}/{ensaio} ainda não existe"
    assert resposta.json() == {"linha": "D", "ensaio": "selagem", "minimo": 1.5, "maximo": 3.0}
    assert cliente.get("/regras/D", headers=LEITURA).json()["regras"] == {
        "selagem": [1.5, 3.0]
    }


def test_gravar_com_perfil_de_leitura_da_403():
    ok = cliente.put("/regras/A/cof", json={"minimo": 0.1, "maximo": 0.2}, headers=ESCRITA)
    assert ok.status_code == 200
    resposta = cliente.put(
        "/regras/A/cof", json={"minimo": 0.0, "maximo": 9.0}, headers=LEITURA
    )
    assert resposta.status_code == 403
    assert resposta.json() == {"detail": "Sem permissão de escrita"}
    assert cliente.get("/regras/A", headers=LEITURA).json()["regras"]["cof"] == [0.1, 0.2]


def test_rotas_usam_a_dependencia_de_regras():
    falsas = {"Z": {"gramatura": [10.0, 12.0]}}
    ex.app.dependency_overrides[ex.obter_regras] = lambda: falsas
    resposta = cliente.get("/regras/Z", headers=LEITURA)
    assert resposta.status_code == 200, "Use Depends(obter_regras) em vez de REGRAS direto"
    assert resposta.json()["regras"] == {"gramatura": [10.0, 12.0]}
    cliente.put("/regras/Z/cof", json={"minimo": 0.2, "maximo": 0.3}, headers=ESCRITA)
    assert falsas["Z"]["cof"] == [0.2, 0.3]
    assert "Z" not in ex.REGRAS
