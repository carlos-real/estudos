import pytest

from _curso import carregar

ex = carregar(__file__, "ex14_tempo_de_producao")


@pytest.mark.parametrize(
    ("metros", "velocidade", "esperado"),
    [
        (12000, 150, 80),
        (12500, 150, 84),
        (100, 200, 1),
        (9000, 150, 60),
    ],
)
def test_minutos_arredondados_para_cima(metros, velocidade, esperado):
    resultado = ex.minutos_de_producao(metros, velocidade)
    assert resultado == esperado, (
        f"{metros} m a {velocidade} m/min: esperado {esperado} min, deu {resultado}. "
        "Qualquer fração de minuto conta como minuto inteiro (math.ceil)."
    )


@pytest.mark.parametrize(
    ("metros", "velocidade", "esperado"),
    [
        (12000, 150, "1h20min"),
        (12500, 150, "1h24min"),
        (100, 200, "0h01min"),
        (9000, 150, "1h00min"),
        (45000, 120, "6h15min"),
    ],
)
def test_tempo_formatado(metros, velocidade, esperado):
    assert ex.tempo_de_producao(metros, velocidade) == esperado


@pytest.mark.parametrize(
    ("hora", "minuto", "metros", "velocidade", "esperado"),
    [
        (8, 0, 12500, 150, "09:24"),
        (7, 5, 100, 200, "07:06"),
        (22, 50, 12500, 150, "00:14"),
        (23, 59, 9000, 150, "00:59"),
    ],
)
def test_horario_de_termino(hora, minuto, metros, velocidade, esperado):
    resultado = ex.horario_termino(hora, minuto, metros, velocidade)
    assert resultado == esperado, (
        f"Começando {hora:02d}:{minuto:02d}, esperado {esperado}, deu {resultado!r}."
    )
