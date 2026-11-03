from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_validade_laudo")

EMISSAO = date(2026, 10, 29)


def test_vencimento_padrao_de_180_dias():
    assert ex.data_vencimento(EMISSAO) == date(2027, 4, 27)


@pytest.mark.parametrize(
    ("emissao", "dias", "esperado"),
    [
        (date(2026, 1, 31), 30, date(2026, 3, 2)),  # atravessa fevereiro
        (date(2027, 12, 20), 15, date(2028, 1, 4)),  # vira o ano
        (date(2028, 2, 28), 1, date(2028, 2, 29)),  # ano bissexto
    ],
)
def test_vencimento_com_outras_validades(emissao, dias, esperado):
    assert ex.data_vencimento(emissao, dias) == esperado


def test_vencimento_devolve_date():
    assert isinstance(ex.data_vencimento(EMISSAO), date)


@pytest.mark.parametrize(
    ("hoje", "esperado"),
    [
        (date(2026, 10, 29), True),  # dia da emissão
        (date(2027, 4, 26), True),
        (date(2027, 4, 27), True),  # no dia do vencimento ainda vale
        (date(2027, 4, 28), False),
        (date(2028, 1, 1), False),
    ],
)
def test_laudo_valido(hoje, esperado):
    assert ex.laudo_valido(EMISSAO, hoje) is esperado, f"hoje = {hoje}"


def test_laudo_valido_com_validade_curta():
    assert ex.laudo_valido(EMISSAO, date(2026, 11, 10), dias_validade=10) is False
    assert ex.laudo_valido(EMISSAO, date(2026, 11, 8), dias_validade=10) is True


@pytest.mark.parametrize(
    ("hoje", "esperado"),
    [
        (date(2026, 10, 29), 180),
        (date(2027, 4, 20), 7),
        (date(2027, 4, 27), 0),
        (date(2027, 5, 1), -4),
    ],
)
def test_dias_para_vencer(hoje, esperado):
    resultado = ex.dias_para_vencer(EMISSAO, hoje)
    assert resultado == esperado
    assert isinstance(resultado, int), "Devolva um int (use .days do timedelta)"
