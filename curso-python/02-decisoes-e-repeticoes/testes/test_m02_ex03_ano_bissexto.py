import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_ano_bissexto")


@pytest.mark.parametrize(
    ("ano", "esperado"),
    [
        (2024, True),
        (2023, False),
        (2028, True),
        (1900, False),
        (2100, False),
        (2000, True),
        (1600, True),
    ],
)
def test_eh_bissexto(ano, esperado):
    resultado = ex.eh_bissexto(ano)
    assert resultado is esperado, f"eh_bissexto({ano}) devolveu {resultado!r}."


def test_seculo_nao_divisivel_por_400_nao_e_bissexto():
    assert ex.eh_bissexto(1900) is False, (
        "1900 é divisível por 4, mas também por 100 (e não por 400): não é bissexto."
    )


@pytest.mark.parametrize(("ano", "dias"), [(2024, 366), (2023, 365), (2000, 366), (1900, 365)])
def test_dias_no_ano(ano, dias):
    assert ex.dias_no_ano(ano) == dias
