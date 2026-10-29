"""Exemplo 03 — Código que usa a rede, testado SEM internet.

Duas funções que consultam APIs públicas brasileiras e dois jeitos de testá-las:
  1. injeção de dependência: a função recebe a "sessão" como parâmetro;
  2. monkeypatch: o teste troca requests.get por uma função falsa.

Rode os testes deste arquivo com qualquer um dos comandos:
    python exemplos/03_cliente_testavel.py
    python -m pytest exemplos/03_cliente_testavel.py -v
"""

import sys

import pytest
import requests

URL_FERIADOS = "https://brasilapi.com.br/api/feriados/v1/{ano}"
URL_CEP = "https://viacep.com.br/ws/{cep}/json/"


# ----------------------------------------------------------------------------
# Código de produção
# ----------------------------------------------------------------------------
def buscar_feriados(ano: int, sessao: requests.Session | None = None) -> list[str]:
    """Devolve 'dd/mm - nome' de cada feriado nacional do ano.

    `sessao` é opcional: no programa real fica None (usamos uma sessão de
    verdade); no teste passamos uma sessão FALSA, que não acessa a internet.
    """
    if sessao is None:
        sessao = requests.Session()
    resposta = sessao.get(URL_FERIADOS.format(ano=ano), timeout=10)
    resposta.raise_for_status()
    feriados = []
    for item in resposta.json():
        _, mes, dia = item["date"].split("-")
        feriados.append(f"{dia}/{mes} - {item['name']}")
    return feriados


def cidade_do_cep(cep: str) -> str:
    """Consulta o ViaCEP e devolve 'Cidade/UF'. Usa requests.get direto."""
    digitos = cep.replace("-", "").strip()
    resposta = requests.get(URL_CEP.format(cep=digitos), timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    if dados.get("erro"):
        raise ValueError(f"CEP não encontrado: {cep}")
    return f"{dados['localidade']}/{dados['uf']}"


# ----------------------------------------------------------------------------
# Dublês de teste: objetos que IMITAM requests.Response e requests.Session
# ----------------------------------------------------------------------------
class RespostaFalsa:
    def __init__(self, dados, status_code: int = 200):
        self.dados = dados
        self.status_code = status_code

    def json(self):
        return self.dados

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")


class SessaoFalsa:
    """Guarda as chamadas recebidas e devolve sempre a mesma resposta."""

    def __init__(self, resposta: RespostaFalsa):
        self.resposta = resposta
        self.chamadas = []

    def get(self, url, **kwargs):
        self.chamadas.append((url, kwargs))
        return self.resposta


# ----------------------------------------------------------------------------
# Testes
# ----------------------------------------------------------------------------
def test_formata_os_feriados():
    dados = [
        {"date": "2026-01-01", "name": "Confraternização mundial"},
        {"date": "2026-04-21", "name": "Tiradentes"},
    ]
    sessao = SessaoFalsa(RespostaFalsa(dados))
    assert buscar_feriados(2026, sessao) == [
        "01/01 - Confraternização mundial",
        "21/04 - Tiradentes",
    ]


def test_monta_a_url_e_usa_timeout():
    sessao = SessaoFalsa(RespostaFalsa([]))
    buscar_feriados(2027, sessao)
    url, kwargs = sessao.chamadas[0]
    assert url == "https://brasilapi.com.br/api/feriados/v1/2027"
    assert kwargs["timeout"] == 10


def test_erro_http_nao_e_engolido():
    sessao = SessaoFalsa(RespostaFalsa({"message": "fora do ar"}, status_code=500))
    with pytest.raises(requests.HTTPError):
        buscar_feriados(2026, sessao)


def test_cidade_do_cep_com_monkeypatch(monkeypatch):
    def get_falso(url, timeout):
        assert url == "https://viacep.com.br/ws/01001000/json/"
        return RespostaFalsa({"localidade": "São Paulo", "uf": "SP"})

    monkeypatch.setattr(requests, "get", get_falso)  # desfeito no fim do teste
    assert cidade_do_cep("01001-000") == "São Paulo/SP"


def test_cep_inexistente(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url, timeout: RespostaFalsa({"erro": True}))
    with pytest.raises(ValueError, match="CEP não encontrado"):
        cidade_do_cep("99999-999")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "-p", "no:cacheprovider", "--no-header"]))
