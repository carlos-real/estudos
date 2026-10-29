import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_dividir_conta")


@pytest.mark.parametrize(
    ("total", "pessoas", "servico", "esperado"),
    [
        (150.0, 4, 10, 41.25),
        (100.0, 3, 10, 36.67),
        (89.9, 2, 0, 44.95),
        (200.0, 1, 12, 224.0),
    ],
)
def test_valor_por_pessoa(total, pessoas, servico, esperado):
    resultado = ex.valor_por_pessoa(total, pessoas, servico)
    assert resultado == pytest.approx(esperado, abs=1e-9), (
        f"Esperado {esperado}, sua função devolveu {resultado}. "
        "Arredondou com round(valor, 2)?"
    )


def test_zero_pessoas_levanta_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        ex.valor_por_pessoa(100.0, 0, 10)


def test_resumo_da_conta():
    assert ex.resumo_conta(100.0, 3, 10) == (
        "Total com 10% de serviço: R$ 110.00 | Por pessoa: R$ 36.67"
    )


def test_resumo_sem_servico():
    assert ex.resumo_conta(80.0, 4, 0) == (
        "Total com 0% de serviço: R$ 80.00 | Por pessoa: R$ 20.00"
    )
