import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_bobina_str_repr")


def test_atributos():
    b = ex.Bobina("L2610", 7, 152.4)
    assert (b.lote, b.numero, b.peso_kg) == ("L2610", 7, pytest.approx(152.4))


@pytest.mark.parametrize(
    ("numero", "esperado"), [(7, "L2610-007"), (42, "L2610-042"), (123, "L2610-123")]
)
def test_codigo_com_tres_digitos(numero, esperado):
    assert ex.Bobina("L2610", numero, 100.0).codigo() == esperado


def test_str_e_amigavel():
    b = ex.Bobina("L2610", 7, 152.44)
    assert str(b) == "Bobina L2610-007 (152.4 kg)"
    assert f"{b}" == "Bobina L2610-007 (152.4 kg)", "f-string usa o __str__"


def test_print_usa_str(capsys):
    print(ex.Bobina("L01", 1, 98.0))
    assert capsys.readouterr().out == "Bobina L01-001 (98.0 kg)\n"


def test_repr_parece_codigo():
    b = ex.Bobina("L2610", 7, 152.4)
    assert repr(b) == "Bobina(lote='L2610', numero=7, peso_kg=152.4)"


def test_lista_de_bobinas_usa_repr():
    bobinas = [ex.Bobina("L1", 1, 10.0), ex.Bobina("L1", 2, 12.5)]
    assert str(bobinas) == (
        "[Bobina(lote='L1', numero=1, peso_kg=10.0), Bobina(lote='L1', numero=2, peso_kg=12.5)]"
    )


def test_repr_recria_o_objeto():
    original = ex.Bobina("L9", 3, 77.7)
    copia = eval(repr(original), {"Bobina": ex.Bobina})
    assert (copia.lote, copia.numero, copia.peso_kg) == ("L9", 3, 77.7)
