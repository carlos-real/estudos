import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_anos_para_dobrar")


@pytest.mark.parametrize(
    ("taxa", "anos"),
    [(10, 8), (100, 1), (6, 12), (12, 7), (1, 70)],
)
def test_anos_para_dobrar(taxa, anos):
    resultado = ex.anos_para_dobrar(taxa)
    assert resultado == anos, f"Com {taxa}% ao ano, esperado {anos} anos, deu {resultado!r}."


@pytest.mark.parametrize("taxa", [0, -5])
def test_taxa_nao_positiva_devolve_menos_um(taxa):
    assert ex.anos_para_dobrar(taxa) == -1, (
        "Com taxa <= 0 o capital nunca dobra: devolva -1 ANTES do while "
        "(senão é loop infinito)."
    )


@pytest.mark.parametrize(
    ("saldo", "deposito", "meta", "meses"),
    [
        (0, 500, 3000, 6),
        (1000, 500, 3000, 4),
        (100, 30, 200, 4),
        (2999.5, 0.5, 3000, 1),
    ],
)
def test_meses_para_meta(saldo, deposito, meta, meses):
    assert ex.meses_para_meta(saldo, deposito, meta) == meses


@pytest.mark.parametrize(("saldo", "meta"), [(5000, 3000), (3000, 3000)])
def test_meta_ja_atingida_devolve_zero(saldo, meta):
    assert ex.meses_para_meta(saldo, 100, meta) == 0


@pytest.mark.parametrize("deposito", [0, -10])
def test_deposito_nao_positivo_devolve_menos_um(deposito):
    assert ex.meses_para_meta(0, deposito, 100) == -1
