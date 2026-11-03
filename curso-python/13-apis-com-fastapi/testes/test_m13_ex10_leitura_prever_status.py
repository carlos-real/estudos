import pytest
from fastapi.testclient import TestClient

from _curso import carregar

ex = carregar(__file__, "ex10_leitura_prever_status")
cliente = TestClient(ex.app, raise_server_exceptions=False)

ESPERADO = {
    "1: GET /tolerancias/A": (200, "GET", "/tolerancias/A", None),
    "2: GET /tolerancias/a": (404, "GET", "/tolerancias/a", None),
    "3: GET /tolerancias": (404, "GET", "/tolerancias", None),
    "4: DELETE /tolerancias/A": (405, "DELETE", "/tolerancias/A", None),
    "5: POST /tolerancias/A/validar com {'ensaio': 'cof', 'valor': 0}": (
        422, "POST", "/tolerancias/A/validar", {"ensaio": "cof", "valor": 0}
    ),
    "6: POST /tolerancias/A/validar com {'ensaio': 'espessura', 'valor': '20'}": (
        200, "POST", "/tolerancias/A/validar", {"ensaio": "espessura", "valor": "20"}
    ),
    "7: POST /tolerancias/B/validar com {'ensaio': 'cof', 'valor': 0.25}": (
        500, "POST", "/tolerancias/B/validar", {"ensaio": "cof", "valor": 0.25}
    ),
    "8: GET /bobinas?limite=abc": (422, "GET", "/bobinas?limite=abc", None),
    "9: GET /bobinas?limite=-1": (200, "GET", "/bobinas?limite=-1", None),
}


@pytest.mark.parametrize("chave", list(ESPERADO))
def test_previsao_de_status(chave):
    previsoes = ex.prever_status()
    assert chave in previsoes, f"Faltou prever: {chave}"
    status, metodo, caminho, corpo = ESPERADO[chave]
    real = cliente.request(metodo, caminho, json=corpo).status_code
    assert real == status, "A API do colega foi alterada; desfaça a mudança"
    assert previsoes[chave] == status, (
        f"Para '{chave}' você previu {previsoes[chave]}. Rode a requisição e descubra o porquê."
    )


def test_previsao_do_json():
    assert cliente.get("/tolerancias/A").json() == {"espessura": [18.0, 22.0], "cof": [0.2, 0.3]}
    assert ex.prever_json_tolerancias_a() == {"espessura": [18.0, 22.0], "cof": [0.2, 0.3]}, (
        "Dica: JSON não tem tuplas"
    )
