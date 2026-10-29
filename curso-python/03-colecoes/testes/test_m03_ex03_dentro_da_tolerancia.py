import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_dentro_da_tolerancia")

TOLERANCIAS = {"A": (45.0, 55.0), "B": (18.0, 22.0), "C": (0.15, 0.30)}


@pytest.mark.parametrize(
    ("valor", "linha"),
    [(50.2, "A"), (20.0, "B"), (0.22, "C")],
)
def test_valor_dentro_da_faixa(valor, linha):
    assert ex.dentro_da_tolerancia(valor, linha, TOLERANCIAS) is True


@pytest.mark.parametrize(
    ("valor", "linha"),
    [(44.9, "A"), (55.1, "A"), (23.5, "B"), (0.31, "C")],
)
def test_valor_fora_da_faixa(valor, linha):
    assert ex.dentro_da_tolerancia(valor, linha, TOLERANCIAS) is False


@pytest.mark.parametrize("valor", [45.0, 55.0])
def test_limites_contam_como_dentro(valor):
    assert ex.dentro_da_tolerancia(valor, "A", TOLERANCIAS) is True, (
        "Os limites mínimo e máximo também são aceitos (use <=)."
    )


@pytest.mark.parametrize(
    ("valor", "linha", "esperado"),
    [(50.0, " a ", True), (60.0, "a", False), (21.0, "B ", True), (0.10, " c", False)],
)
def test_nome_da_linha_e_normalizado(valor, linha, esperado):
    assert ex.dentro_da_tolerancia(valor, linha, TOLERANCIAS) is esperado, (
        "Linha com espaços ou minúscula deve ser encontrada (use strip e upper)."
    )


def test_linha_inexistente_devolve_none():
    assert ex.dentro_da_tolerancia(30.0, "Z", TOLERANCIAS) is None


def test_dicionario_vazio_devolve_none():
    assert ex.dentro_da_tolerancia(30.0, "A", {}) is None
