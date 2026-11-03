from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex01_ola_api")
cliente = TestClient(ex.app)


def test_raiz():
    resposta = cliente.get("/")
    assert resposta.status_code == 200, "A rota GET / ainda não existe"
    assert resposta.json() == {"mensagem": "API do laboratório no ar"}


def test_saude():
    resposta = cliente.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_versao_usa_a_constante(monkeypatch):
    resposta = cliente.get("/versao")
    assert resposta.status_code == 200
    assert resposta.json() == {"versao": "1.0.0"}
    monkeypatch.setattr(ex, "VERSAO", "2.5.0")
    assert cliente.get("/versao").json() == {"versao": "2.5.0"}, (
        "Use a constante VERSAO em vez de escrever o texto direto"
    )


def test_rotas_aceitam_so_get():
    assert cliente.get("/saude").status_code == 200
    # 405 = a rota existe, mas não para este método
    assert cliente.post("/saude").status_code == 405
