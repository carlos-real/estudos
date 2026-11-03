import pytest
import requests

from _curso import carregar

ex = carregar(__file__, "ex03_buscar_tolerancias")

BASE = "http://api.lab.local"
JSON_LINHA_A = {
    "linha": "A",
    "itens": [
        {"ensaio": "espessura", "minimo": 18.0, "maximo": 22.0},
        {"ensaio": "cof", "minimo": 0.2, "maximo": 0.3},
    ],
}


class RespostaFalsa:
    def __init__(self, dados, status_code=200):
        self.dados = dados
        self.status_code = status_code

    def json(self):
        return self.dados

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error", response=self)


class SessaoFalsa:
    """Imita requests.Session: registra as chamadas e devolve uma resposta pronta."""

    def __init__(self, resposta):
        self.resposta = resposta
        self.chamadas = []

    def get(self, url, **kwargs):
        self.chamadas.append({"url": url, **kwargs})
        return self.resposta


def test_converte_itens_em_dicionario_de_tuplas():
    sessao = SessaoFalsa(RespostaFalsa(JSON_LINHA_A))
    resultado = ex.buscar_tolerancias(sessao, BASE, "A")
    assert resultado == {"espessura": (18.0, 22.0), "cof": (0.2, 0.3)}


def test_chama_a_url_certa_com_params_e_timeout():
    sessao = SessaoFalsa(RespostaFalsa(JSON_LINHA_A))
    ex.buscar_tolerancias(sessao, BASE, "A", timeout=3)
    assert len(sessao.chamadas) == 1, "Era esperada exatamente uma chamada a sessao.get"
    chamada = sessao.chamadas[0]
    assert chamada["url"] == "http://api.lab.local/tolerancias"
    assert chamada["params"] == {"linha": "A"}
    assert chamada["timeout"] == 3


def test_timeout_padrao_e_10_segundos():
    sessao = SessaoFalsa(RespostaFalsa(JSON_LINHA_A))
    ex.buscar_tolerancias(sessao, BASE, "A")
    assert sessao.chamadas[0]["timeout"] == 10, "Sempre passe timeout= nas chamadas HTTP"


def test_linha_minuscula_vira_maiuscula():
    sessao = SessaoFalsa(RespostaFalsa({"linha": "B", "itens": []}))
    assert ex.buscar_tolerancias(sessao, BASE, "b") == {}
    assert sessao.chamadas[0]["params"] == {"linha": "B"}


@pytest.mark.parametrize("linha", ["E", "Z", "AB", ""])
def test_linha_invalida_nao_chama_a_rede(linha):
    sessao = SessaoFalsa(RespostaFalsa(JSON_LINHA_A))
    with pytest.raises(ValueError):
        ex.buscar_tolerancias(sessao, BASE, linha)
    assert sessao.chamadas == [], "A validação deve acontecer ANTES de chamar a API"


def test_erro_http_e_propagado():
    sessao = SessaoFalsa(RespostaFalsa({"erro": "fora do ar"}, status_code=503))
    with pytest.raises(requests.HTTPError):
        ex.buscar_tolerancias(sessao, BASE, "C")
