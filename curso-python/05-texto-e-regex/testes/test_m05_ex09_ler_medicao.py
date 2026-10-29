import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_ler_medicao")


@pytest.mark.parametrize(
    ("linha", "ensaio", "valor", "unidade"),
    [
        ("Espessura: 25,4 µm", "Espessura", 25.4, "µm"),
        ("Gramatura = 23,10 g/m²", "Gramatura", 23.1, "g/m²"),
        ("  Selagem = 1.250,5 N/15 mm ", "Selagem", 1250.5, "N/15 mm"),
        ("Variação: -1,5 %", "Variação", -1.5, "%"),
        ("Tração MD:32 MPa", "Tração MD", 32.0, "MPa"),
    ],
)
def test_linhas_validas(linha, ensaio, valor, unidade):
    resultado = ex.ler_medicao(linha)
    assert resultado is not None, f"{linha!r} está no formato certo"
    assert resultado["ensaio"] == ensaio
    assert resultado["valor"] == pytest.approx(valor)
    assert resultado["unidade"] == unidade


def test_sem_unidade():
    assert ex.ler_medicao("COF estático: 0,21") == {
        "ensaio": "COF estático",
        "valor": 0.21,
        "unidade": "",
    }


def test_valor_e_float():
    assert isinstance(ex.ler_medicao("Peso: 980 kg")["valor"], float)


@pytest.mark.parametrize(
    "linha",
    [
        "Observação: COF liberado",
        "Espessura 25,4 µm",
        ": 25,4",
        "   ",
        "",
    ],
)
def test_linhas_fora_do_formato_devolvem_none(linha):
    assert ex.ler_medicao(linha) is None
