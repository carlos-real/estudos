import pytest
import requests

from _curso import carregar

ex = carregar(__file__, "ex04_com_retentativas")


class FuncaoInstavel:
    """Falha `falhas` vezes com o erro dado e depois devolve `resultado`."""

    def __init__(self, falhas, erro=requests.ConnectionError, resultado="ok"):
        self.falhas = falhas
        self.erro = erro
        self.resultado = resultado
        self.chamadas = 0

    def __call__(self):
        self.chamadas += 1
        if self.chamadas <= self.falhas:
            raise self.erro(f"falha simulada nº {self.chamadas}")
        return self.resultado


def test_sucesso_de_primeira_nao_espera():
    funcao = FuncaoInstavel(falhas=0, resultado={"linha": "A"})
    esperas = []
    assert ex.com_retentativas(funcao, dormir=esperas.append) == {"linha": "A"}
    assert funcao.chamadas == 1
    assert esperas == []


def test_falha_duas_vezes_e_depois_funciona():
    funcao = FuncaoInstavel(falhas=2)
    esperas = []
    resultado = ex.com_retentativas(funcao, tentativas=3, espera=1.0, dormir=esperas.append)
    assert resultado == "ok"
    assert funcao.chamadas == 3
    assert esperas == [1.0, 2.0], "As esperas devem dobrar: espera, espera*2, ..."


def test_timeout_tambem_e_repetido():
    funcao = FuncaoInstavel(falhas=1, erro=requests.Timeout)
    esperas = []
    assert ex.com_retentativas(funcao, espera=0.5, dormir=esperas.append) == "ok"
    assert esperas == [0.5]


def test_todas_falham_relanca_sem_esperar_depois_da_ultima():
    funcao = FuncaoInstavel(falhas=10)
    esperas = []
    with pytest.raises(requests.ConnectionError, match="nº 4"):
        ex.com_retentativas(funcao, tentativas=4, espera=2.0, dormir=esperas.append)
    assert funcao.chamadas == 4
    assert esperas == [2.0, 4.0, 8.0], "Não durma depois da última tentativa"


def test_uma_tentativa_so_nao_espera():
    funcao = FuncaoInstavel(falhas=1)
    esperas = []
    with pytest.raises(requests.ConnectionError):
        ex.com_retentativas(funcao, tentativas=1, dormir=esperas.append)
    assert esperas == []


@pytest.mark.parametrize("erro", [requests.HTTPError, ValueError, KeyError])
def test_outros_erros_sobem_sem_nova_tentativa(erro):
    funcao = FuncaoInstavel(falhas=1, erro=erro)
    esperas = []
    with pytest.raises(erro):
        ex.com_retentativas(funcao, tentativas=3, dormir=esperas.append)
    assert funcao.chamadas == 1, f"{erro.__name__} não deve ser repetido"
    assert esperas == []


@pytest.mark.parametrize("tentativas", [0, -1])
def test_tentativas_invalidas(tentativas):
    with pytest.raises(ValueError):
        ex.com_retentativas(lambda: "ok", tentativas=tentativas, dormir=lambda s: None)
