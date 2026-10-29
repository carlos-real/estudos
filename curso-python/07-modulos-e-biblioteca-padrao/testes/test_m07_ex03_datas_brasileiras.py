from datetime import date, datetime

import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_datas_brasileiras")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("29/10/2026", date(2026, 10, 29)),
        (" 01/01/2027 ", date(2027, 1, 1)),
        ("29/02/2028", date(2028, 2, 29)),
    ],
)
def test_ler_data_br(texto, esperado):
    resultado = ex.ler_data_br(texto)
    assert resultado == esperado
    assert type(resultado) is date, "Devolva date (use .date() no resultado do strptime)"


@pytest.mark.parametrize("texto", ["31/02/2026", "2026-10-29", "29/13/2026", "ontem"])
def test_ler_data_br_invalida_gera_value_error(texto):
    with pytest.raises(ValueError):
        ex.ler_data_br(texto)


@pytest.mark.parametrize(
    ("data", "esperado"),
    [(date(2026, 3, 5), "05/03/2026"), (date(2026, 12, 31), "31/12/2026")],
)
def test_formatar_data_br(data, esperado):
    assert ex.formatar_data_br(data) == esperado


def test_ida_e_volta():
    assert ex.formatar_data_br(ex.ler_data_br("07/08/2026")) == "07/08/2026"


def test_ler_data_hora_br():
    assert ex.ler_data_hora_br("29/10/2026 14:30") == datetime(2026, 10, 29, 14, 30)
    assert ex.ler_data_hora_br(" 01/11/2026 07:05 ") == datetime(2026, 11, 1, 7, 5)


def test_ler_data_hora_br_sem_hora_gera_value_error():
    with pytest.raises(ValueError):
        ex.ler_data_hora_br("29/10/2026")


@pytest.mark.parametrize(
    ("data", "esperado"),
    [
        (date(2026, 10, 26), "segunda"),
        (date(2026, 10, 27), "terça"),
        (date(2026, 10, 29), "quinta"),
        (date(2026, 10, 31), "sábado"),
        (date(2026, 11, 1), "domingo"),
    ],
)
def test_dia_da_semana(data, esperado):
    assert ex.dia_da_semana(data) == esperado
