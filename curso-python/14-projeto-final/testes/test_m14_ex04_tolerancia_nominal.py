import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_tolerancia_nominal")


@pytest.mark.parametrize(
    ("nominal", "percentual", "esperado"),
    [
        (40, 10, (36.0, 44.0)),
        (37, 10, (33.3, 40.7)),
        (41.6, 8, (38.272, 44.928)),
        (46.3, 5, (43.985, 48.615)),
    ],
)
def test_limites_sem_lixo_de_float(nominal, percentual, esperado):
    assert ex.limites_nominal(nominal, percentual) == esperado, (
        "Arredonde cada limite com round(x, 4) para tirar o lixo do float."
    )


@pytest.mark.parametrize(("nominal", "percentual"), [(0, 10), (40, 0), (-40, 10), (40, -5)])
def test_limites_com_entrada_invalida(nominal, percentual):
    with pytest.raises(ValueError):
        ex.limites_nominal(nominal, percentual)


@pytest.mark.parametrize("valor", [36.0, 41.2, 44.0])
def test_dentro_da_faixa_e_nos_limites(valor):
    assert ex.verificar_nominal("espessura", valor, 40, 10) is None


def test_valor_no_limite_com_float_traicoeiro():
    assert ex.verificar_nominal("gramatura", 33.3, 37, 10) is None
    assert ex.verificar_nominal("gramatura", 48.615, 46.3, 5) is None


def test_acima_da_faixa():
    esperado = "espessura 44.8 fora de 40 ± 10% (36 a 44)"
    assert ex.verificar_nominal("espessura", 44.8, 40, 10) == esperado


def test_abaixo_da_faixa():
    esperado = "gramatura 64.9 fora de 70.5 ± 7% (65.565 a 75.435)"
    assert ex.verificar_nominal("gramatura", 64.9, 70.5, 7) == esperado
