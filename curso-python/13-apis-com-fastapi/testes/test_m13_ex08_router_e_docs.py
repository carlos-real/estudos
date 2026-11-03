from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex08_router_e_docs")
cliente = TestClient(ex.app)


def rota_da_lista(esquema):
    """Aceita /ensaios e /ensaios/ (depende de como o caminho foi escrito)."""
    for caminho in ("/ensaios/", "/ensaios"):
        if caminho in esquema["paths"]:
            return esquema["paths"][caminho]
    raise AssertionError("A rota da lista de ensaios não aparece na documentação")


def test_lista_de_ensaios():
    resposta = cliente.get("/ensaios/")
    assert resposta.status_code == 200, "A rota GET /ensaios/ ainda não existe"
    assert resposta.json() == ["cof", "espessura", "selagem", "tracao"]


def test_detalhe_de_um_ensaio():
    resposta = cliente.get("/ensaios/tracao")
    assert resposta.status_code == 200
    assert resposta.json() == {"nome": "tracao", "unidade": "MPa", "norma": "ASTM D882"}


def test_ensaio_inexistente():
    assert cliente.get("/ensaios/cof").status_code == 200, "A rota /ensaios/{nome} não existe"
    resposta = cliente.get("/ensaios/dureza")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Ensaio dureza não cadastrado"}


def test_titulo_e_versao_na_documentacao():
    info = cliente.get("/openapi.json").json()["info"]
    assert info["title"] == "API do Laboratório"
    assert info["version"] == "1.0.0"


def test_tags_e_resumos():
    esquema = cliente.get("/openapi.json").json()
    lista = rota_da_lista(esquema)["get"]
    detalhe = esquema["paths"]["/ensaios/{nome}"]["get"]
    assert lista["tags"] == ["ensaios"]
    assert detalhe["tags"] == ["ensaios"]
    assert lista["summary"] == "Lista os ensaios"
    assert detalhe["summary"] == "Detalhes de um ensaio"
