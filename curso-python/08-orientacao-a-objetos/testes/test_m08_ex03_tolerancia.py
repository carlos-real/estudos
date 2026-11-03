import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_tolerancia")


def test_guarda_limites():
    t = ex.Tolerancia(0.10, 0.30)
    assert (t.minimo, t.maximo) == (0.10, 0.30)
    so_minimo = ex.Tolerancia(minimo=20)
    assert (so_minimo.minimo, so_minimo.maximo) == (20, None)


@pytest.mark.parametrize(
    ("valor", "esperado"), [(0.10, True), (0.30, True), (0.2, True), (0.09, False), (0.31, False)]
)
def test_aprova_faixa(valor, esperado):
    assert ex.Tolerancia(0.10, 0.30).aprova(valor) is esperado


@pytest.mark.parametrize(("valor", "esperado"), [(20, True), (35.2, True), (19.9, False)])
def test_aprova_so_minimo(valor, esperado):
    assert ex.Tolerancia(minimo=20).aprova(valor) is esperado


@pytest.mark.parametrize(("valor", "esperado"), [(0.0, True), (0.3, True), (0.31, False)])
def test_aprova_so_maximo(valor, esperado):
    assert ex.Tolerancia(maximo=0.3).aprova(valor) is esperado


def test_limite_zero_e_valido():
    t = ex.Tolerancia(minimo=0)
    assert t.aprova(-0.1) is False, "Zero é limite: use 'is not None', não 'if self.minimo'"


@pytest.mark.parametrize(
    ("kwargs", "esperado"),
    [
        ({"minimo": 0.1, "maximo": 0.3}, "0.10 a 0.30"),
        ({"minimo": 20}, "mín. 20.00"),
        ({"maximo": 0.3}, "máx. 0.30"),
    ],
)
def test_descricao(kwargs, esperado):
    assert ex.Tolerancia(**kwargs).descricao() == esperado


@pytest.mark.parametrize("kwargs", [{}, {"minimo": 30, "maximo": 20}])
def test_limites_invalidos_geram_value_error(kwargs):
    with pytest.raises(ValueError):
        ex.Tolerancia(**kwargs)
