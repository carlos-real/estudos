from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_corrigir_dias_uteis")

FINADOS = date(2026, 11, 2)
FERIADOS = {FINADOS, date(2026, 11, 20)}


def test_previsao_da_versao_com_defeito():
    assert ex.previsao_versao_com_defeito() == date(2026, 10, 31), (
        "Rode o código do colega no terminal para conferir sua previsão."
    )


@pytest.mark.parametrize(
    ("dia", "esperado"),
    [
        (date(2026, 10, 26), True),  # segunda
        (date(2026, 10, 30), True),  # sexta
        (date(2026, 10, 31), False),  # sábado
        (date(2026, 11, 1), False),  # domingo
    ],
)
def test_eh_dia_util_sem_feriados(dia, esperado):
    assert ex.eh_dia_util(dia) is esperado


def test_eh_dia_util_com_feriado():
    assert ex.eh_dia_util(FINADOS, FERIADOS) is False
    assert ex.eh_dia_util(FINADOS) is True


@pytest.mark.parametrize(
    ("inicio", "dias", "feriados", "esperado"),
    [
        (date(2026, 10, 29), 1, None, date(2026, 10, 30)),
        (date(2026, 10, 29), 2, None, date(2026, 11, 2)),
        (date(2026, 10, 29), 2, FERIADOS, date(2026, 11, 3)),
        (date(2026, 10, 29), 5, FERIADOS, date(2026, 11, 6)),
        (date(2026, 10, 31), 1, None, date(2026, 11, 2)),  # começa no sábado
        (date(2026, 10, 29), 0, None, date(2026, 10, 29)),
    ],
)
def test_somar_dias_uteis(inicio, dias, feriados, esperado):
    resultado = ex.somar_dias_uteis(inicio, dias, feriados)
    assert resultado == esperado
    assert resultado.weekday() < 5 or dias == 0, "Prazo nunca deve cair em fim de semana"


@pytest.mark.parametrize(
    ("inicio", "fim", "feriados", "esperado"),
    [
        (date(2026, 10, 29), date(2026, 10, 30), None, 1),
        (date(2026, 10, 29), date(2026, 11, 5), None, 5),
        (date(2026, 10, 29), date(2026, 11, 5), FERIADOS, 4),
        (date(2026, 10, 30), date(2026, 11, 1), None, 0),  # só fim de semana
        (date(2026, 10, 29), date(2026, 10, 29), None, 0),
        (date(2026, 11, 5), date(2026, 10, 29), None, 0),  # fim antes do início
    ],
)
def test_dias_uteis_entre(inicio, fim, feriados, esperado):
    assert ex.dias_uteis_entre(inicio, fim, feriados) == esperado
