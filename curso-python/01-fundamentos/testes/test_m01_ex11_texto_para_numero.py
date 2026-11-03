import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_texto_para_numero")


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        (" 25,4 ", 25.4),
        ("1250.5", 1250.5),
        ("12,5 KG", 12.5),
        ("980kg", 980.0),
        ("  7 Kg ", 7.0),
        ("0,05", 0.05),
    ],
)
def test_converte_textos_validos(texto, esperado):
    resultado = ex.texto_para_numero(texto)
    assert resultado == pytest.approx(esperado), (
        f"texto_para_numero({texto!r}) devolveu {resultado!r}."
    )


@pytest.mark.parametrize("texto", ["abc", "", "kg", "doze"])
def test_texto_invalido_levanta_value_error(texto):
    with pytest.raises(ValueError):
        ex.texto_para_numero(texto)


def test_soma_classica_do_float_fica_exata():
    resultado = ex.somar_pesos("0,1", "0,2")
    assert resultado == 0.3, f"Deu {resultado!r}. Faltou o round(..., 2)?"


def test_soma_de_pesos_com_unidade():
    assert ex.somar_pesos("1250,5 kg", "749,5") == pytest.approx(2000.0)


def test_soma_com_peso_invalido_levanta_value_error():
    with pytest.raises(ValueError):
        ex.somar_pesos("10,0", "dez")
