import pytest
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex02_parametros_caminho")
cliente = TestClient(ex.app)


@pytest.mark.parametrize(("numero", "dobro"), [(21, 42), (0, 0), (-5, -10), (1000, 2000)])
def test_dobro(numero, dobro):
    resposta = cliente.get(f"/dobro/{numero}")
    assert resposta.status_code == 200, "A rota /dobro/{numero} ainda não existe"
    assert resposta.json() == {"numero": numero, "dobro": dobro}


def test_dobro_devolve_numero_e_nao_texto():
    dados = cliente.get("/dobro/21").json()
    assert dados["dobro"] == 42, "Declare numero: int (sem isso, '21' * 2 vira '2121')"


def test_dobro_recusa_texto_com_422():
    assert cliente.get("/dobro/7").status_code == 200
    assert cliente.get("/dobro/abc").status_code == 422
    assert cliente.get("/dobro/2.5").status_code == 422


@pytest.mark.parametrize("nome", ["Carla", "Ana Paula", "João"])
def test_saudacao(nome):
    resposta = cliente.get(f"/saudacao/{nome}")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": f"Olá, {nome}!"}
