import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_tolerancia_da_linha")


@pytest.mark.parametrize(
    ("linha", "esperado"),
    [("A", 5.0), ("B", 5.0), ("C", 8.0), ("D", 10.0)],
)
def test_linhas_conhecidas(linha, esperado):
    assert ex.tolerancia_da_linha(linha) == pytest.approx(esperado)


@pytest.mark.parametrize(
    ("linha", "esperado"),
    [(" b ", 5.0), ("c", 8.0), ("  d", 10.0)],
)
def test_ignora_espacos_e_minusculas(linha, esperado):
    resultado = ex.tolerancia_da_linha(linha)
    assert resultado == pytest.approx(esperado), (
        f"tolerancia_da_linha({linha!r}) devolveu {resultado!r}. "
        "Normalizou com strip().upper()?"
    )


@pytest.mark.parametrize("linha", ["E", "", "AB", "linha A"])
def test_linha_desconhecida_devolve_none(linha):
    resultado = ex.tolerancia_da_linha(linha)
    assert resultado is None, (
        f"tolerancia_da_linha({linha!r}) deveria ser None, deu {resultado!r}."
    )
