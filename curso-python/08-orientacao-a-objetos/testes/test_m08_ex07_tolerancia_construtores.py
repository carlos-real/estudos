import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_tolerancia_construtores")
T = ex.Tolerancia


def test_init_guarda_floats():
    t = T(20, 30)
    assert (t.minimo, t.maximo) == (20.0, 30.0)
    assert type(t.minimo) is float


def test_init_minimo_maior_que_maximo():
    with pytest.raises(ValueError):
        T(30, 20)


@pytest.mark.parametrize(
    ("nominal", "percentual", "minimo", "maximo"),
    [(25, 10, 22.5, 27.5), (40, 5, 38.0, 42.0), (18.4, 0, 18.4, 18.4)],
)
def test_por_nominal(nominal, percentual, minimo, maximo):
    t = T.por_nominal(nominal, percentual)
    assert isinstance(t, T)
    assert t.minimo == pytest.approx(minimo)
    assert t.maximo == pytest.approx(maximo)


def test_por_nominal_percentual_negativo():
    with pytest.raises(ValueError):
        T.por_nominal(25, -1)


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("1.250,5", 1250.5), ("0,10", 0.1), (" 25 ", 25.0), ("12.000", 12000.0)],
)
def test_converter_numero_e_staticmethod(texto, esperado):
    assert T.converter_numero(texto) == pytest.approx(esperado)
    assert T(1, 2).converter_numero(texto) == pytest.approx(esperado)


@pytest.mark.parametrize(
    ("texto", "minimo", "maximo"),
    [
        ("0,10 a 0,30", 0.10, 0.30),
        ("  20 a 1.000 ", 20.0, 1000.0),
        ("25 ± 10%", 22.5, 27.5),
        ("25+-10 %", 22.5, 27.5),
        ("40,0 ± 5%", 38.0, 42.0),
    ],
)
def test_de_texto(texto, minimo, maximo):
    t = T.de_texto(texto)
    assert t.minimo == pytest.approx(minimo)
    assert t.maximo == pytest.approx(maximo)


@pytest.mark.parametrize("texto", ["25", "0,10 - 0,30", "25 ± 10", "vinte a trinta"])
def test_de_texto_formato_invalido(texto):
    with pytest.raises(ValueError):
        T.de_texto(texto)


def test_aprova():
    t = T.de_texto("0,10 a 0,30")
    assert [t.aprova(v) for v in (0.09, 0.10, 0.2, 0.30, 0.31)] == [
        False,
        True,
        True,
        True,
        False,
    ]


def test_repr():
    assert repr(T(20, 30)) == "Tolerancia(minimo=20.0, maximo=30.0)"


def test_classmethods_funcionam_em_subclasse():
    class ToleranciaEspessura(T):
        pass

    assert type(ToleranciaEspessura.por_nominal(25, 10)) is ToleranciaEspessura, (
        "Use cls(...) no classmethod, e não Tolerancia(...)"
    )
    assert type(ToleranciaEspessura.de_texto("20 a 30")) is ToleranciaEspessura
