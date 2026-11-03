import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_comprimento_bobina")


def test_bobina_padrao_de_25_micra():
    assert ex.comprimento_bobina(600, 152, 25) == pytest.approx(10583.9)


@pytest.mark.parametrize(
    ("externo", "tubete", "espessura", "esperado"),
    [
        (1000, 76, 50, 15617.2),
        (400, 152, 12, 8959.8),
        (500, 76, 20, 9590.7),
    ],
)
def test_outras_bobinas(externo, tubete, espessura, esperado):
    resultado = ex.comprimento_bobina(externo, tubete, espessura)
    assert resultado == pytest.approx(esperado), (
        "Confira as conversões: mm → m (÷ 1000) e µm → m (÷ 1.000.000)."
    )


def test_comprimento_vem_arredondado_em_uma_casa():
    resultado = ex.comprimento_bobina(600, 152, 25)
    assert resultado == round(resultado, 1)


@pytest.mark.parametrize(("externo", "tubete", "espessura"), [(600, 152, 0), (600, 152, -5)])
def test_espessura_invalida_gera_value_error(externo, tubete, espessura):
    with pytest.raises(ValueError):
        ex.comprimento_bobina(externo, tubete, espessura)


@pytest.mark.parametrize("tubete", [600, 700])
def test_tubete_maior_ou_igual_ao_externo_gera_value_error(tubete):
    with pytest.raises(ValueError):
        ex.comprimento_bobina(600, tubete, 25)


@pytest.mark.parametrize(
    ("pedido", "por_bobina", "esperado"),
    [(50000, 10583.9, 5), (20000, 10583.9, 2), (10583.9, 10583.9, 1), (1, 10583.9, 1)],
)
def test_bobinas_necessarias_arredonda_para_cima(pedido, por_bobina, esperado):
    assert ex.bobinas_necessarias(pedido, por_bobina) == esperado


def test_bobinas_necessarias_devolve_int():
    assert isinstance(ex.bobinas_necessarias(50000, 10583.9), int)


def test_bobinas_necessarias_com_metros_por_bobina_zero():
    with pytest.raises(ValueError):
        ex.bobinas_necessarias(1000, 0)
