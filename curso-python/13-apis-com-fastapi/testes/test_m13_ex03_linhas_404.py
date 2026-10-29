import pytest
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex03_linhas_404")
cliente = TestClient(ex.app)


def test_lista_de_linhas_em_ordem():
    resposta = cliente.get("/linhas")
    assert resposta.status_code == 200, "A rota GET /linhas ainda não existe"
    assert resposta.json() == ["A", "B", "C", "D"]


def test_detalhe_de_uma_linha():
    resposta = cliente.get("/linhas/C")
    assert resposta.status_code == 200
    assert resposta.json() == {"codigo": "C", "nome": "Laminadora C", "produto": "Laminado PET/PE"}


@pytest.mark.parametrize("pedido", ["b", "B"])
def test_aceita_minuscula(pedido):
    resposta = cliente.get(f"/linhas/{pedido}")
    assert resposta.status_code == 200
    assert resposta.json()["codigo"] == "B"


@pytest.mark.parametrize(("pedido", "letra"), [("z", "Z"), ("E", "E"), ("ab", "AB")])
def test_linha_inexistente_da_404_com_mensagem(pedido, letra):
    assert cliente.get("/linhas/A").status_code == 200, "A rota /linhas/{codigo} não existe"
    resposta = cliente.get(f"/linhas/{pedido}")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": f"Linha {letra} não encontrada"}
