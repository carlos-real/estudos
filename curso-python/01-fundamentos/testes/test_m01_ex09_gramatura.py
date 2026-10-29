import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_gramatura")


def test_gramatura_corpo_de_prova_10_por_10():
    resultado = ex.calcular_gramatura(0.523, 10, 10)
    assert resultado == pytest.approx(52.3, abs=1e-9), (
        f"Esperado 52.3 g/m², sua função devolveu {resultado}. "
        "Converteu cm para m (dividir por 100) e arredondou em 1 casa?"
    )


@pytest.mark.parametrize(
    ("massa", "largura", "comprimento", "esperado"),
    [
        (2.4718, 20, 25, 49.4),
        (1.0, 10, 10, 100.0),
        (0.2, 5, 4, 100.0),
    ],
)
def test_gramatura_varios_tamanhos(massa, largura, comprimento, esperado):
    resultado = ex.calcular_gramatura(massa, largura, comprimento)
    assert resultado == pytest.approx(esperado, abs=1e-9)


def test_peso_da_bobina():
    resultado = ex.peso_bobina_kg(52.3, 600, 4000)
    assert resultado == pytest.approx(125.52, abs=1e-9), (
        f"Esperado 125.52 kg, sua função devolveu {resultado}. Converteu mm para m?"
    )


@pytest.mark.parametrize(
    ("gramatura", "largura_mm", "comprimento_m", "esperado"),
    [
        (40.0, 1000, 1000, 40.0),
        (48.5, 330, 6000, 96.03),
        (52.3, 600, 0, 0.0),
    ],
)
def test_peso_da_bobina_varios_casos(gramatura, largura_mm, comprimento_m, esperado):
    resultado = ex.peso_bobina_kg(gramatura, largura_mm, comprimento_m)
    assert resultado == pytest.approx(esperado, abs=1e-9)
