import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_fatorial")


@pytest.mark.parametrize(
    ("n", "esperado"),
    [(0, 1), (1, 1), (2, 2), (5, 120), (10, 3628800)],
)
def test_fatorial(n, esperado):
    resultado = ex.fatorial(n)
    assert resultado == esperado, f"fatorial({n}) devolveu {resultado!r}."


def test_fatorial_de_negativo_e_none():
    assert ex.fatorial(-3) is None


@pytest.mark.parametrize(("n", "esperado"), [(1, 1), (4, 10), (100, 5050)])
def test_soma_de_1_ate(n, esperado):
    resultado = ex.soma_de_1_ate(n)
    assert resultado == esperado, (
        f"soma_de_1_ate({n}) devolveu {resultado!r}. "
        "O fim do range é exclusivo: range(1, n + 1)."
    )


@pytest.mark.parametrize("n", [0, -5])
def test_soma_com_n_menor_que_1_e_zero(n):
    assert ex.soma_de_1_ate(n) == 0
