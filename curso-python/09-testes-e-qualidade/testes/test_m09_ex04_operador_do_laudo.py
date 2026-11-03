import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_operador_do_laudo")


@pytest.mark.parametrize(
    ("valor_da_variavel", "esperado"),
    [
        ("Maria Souza", "Maria Souza"),
        ("  João Pereira  ", "João Pereira"),
        ("\tAna\n", "Ana"),
    ],
)
def test_operador_definido(monkeypatch, valor_da_variavel, esperado):
    monkeypatch.setenv("LAB_OPERADOR", valor_da_variavel)
    assert ex.operador_atual() == esperado


def test_operador_sem_variavel_de_ambiente(monkeypatch):
    monkeypatch.delenv("LAB_OPERADOR", raising=False)
    assert ex.operador_atual() == "não informado"


def test_operador_com_variavel_vazia(monkeypatch):
    monkeypatch.setenv("LAB_OPERADOR", "   ")
    assert ex.operador_atual() == "não informado"


def test_assinatura_usa_o_operador(monkeypatch):
    monkeypatch.setenv("LAB_OPERADOR", "Maria Souza")
    assert ex.assinatura_laudo("12345") == "OP 12345 | operador: Maria Souza"


def test_assinatura_sem_operador(monkeypatch):
    monkeypatch.delenv("LAB_OPERADOR", raising=False)
    assert ex.assinatura_laudo("777") == "OP 777 | operador: não informado"


def test_variavel_e_lida_na_hora_da_chamada(monkeypatch):
    monkeypatch.setenv("LAB_OPERADOR", "Primeiro")
    assert ex.operador_atual() == "Primeiro"
    monkeypatch.setenv("LAB_OPERADOR", "Segundo")
    assert ex.operador_atual() == "Segundo", "leia os.environ dentro da função"
