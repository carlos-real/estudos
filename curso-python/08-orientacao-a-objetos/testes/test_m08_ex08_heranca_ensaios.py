import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_heranca_ensaios")


def test_filhas_sao_ensaios_e_herdam_atributos():
    e = ex.EnsaioFaixa("espessura", 25, 22.5, 27.5, "µm")
    assert isinstance(e, ex.Ensaio)
    assert (e.nome, e.valor, e.unidade) == ("espessura", 25.0, "µm")
    assert (e.minimo, e.maximo) == (22.5, 27.5)
    assert type(e.valor) is float, "A mãe (via super().__init__) converte para float"


@pytest.mark.parametrize(("valor", "esperado"), [(22.5, True), (27.5, True), (28, False)])
def test_ensaio_faixa(valor, esperado):
    assert ex.EnsaioFaixa("espessura", valor, 22.5, 27.5).aprovado() is esperado


@pytest.mark.parametrize(("valor", "esperado"), [(20, True), (35, True), (19.9, False)])
def test_ensaio_minimo(valor, esperado):
    e = ex.EnsaioMinimo("tração", valor, 20, "MPa")
    assert e.aprovado() is esperado
    assert e.minimo == 20


@pytest.mark.parametrize(("valor", "esperado"), [(0.30, True), (0.1, True), (0.31, False)])
def test_ensaio_maximo(valor, esperado):
    e = ex.EnsaioMaximo("cof", valor, 0.30)
    assert e.aprovado() is esperado
    assert e.maximo == 0.30


@pytest.mark.parametrize(
    ("ensaio", "esperado"),
    [
        (("EnsaioFaixa", "espessura", 25.3, 22.5, 27.5, "µm"), "espessura: 25.30 µm -> APROVADO"),
        (("EnsaioMaximo", "cof", 0.32, 0.30), "cof: 0.32 -> REPROVADO"),
        (("EnsaioMinimo", "tração", 31, 20, "MPa"), "tração: 31.00 MPa -> APROVADO"),
    ],
)
def test_laudo_polimorfico(ensaio, esperado):
    classe, *args = ensaio
    assert getattr(ex, classe)(*args).laudo() == esperado


def test_reprovados_mistura_tipos():
    ensaios = [
        ex.EnsaioFaixa("espessura", 28.0, 22.5, 27.5, "µm"),
        ex.EnsaioMinimo("tração", 25, 20, "MPa"),
        ex.EnsaioMaximo("cof", 0.35, 0.30),
        ex.EnsaioFaixa("gramatura", 23.0, 20.7, 25.3, "g/m²"),
    ]
    assert ex.reprovados(ensaios) == ["espessura", "cof"]


def test_reprovados_lista_vazia_e_todos_aprovados():
    assert ex.reprovados([]) == []
    assert ex.reprovados([ex.EnsaioMaximo("cof", 0.2, 0.3)]) == []


def test_nova_filha_funciona_sem_mudar_a_mae():
    class EnsaioExato(ex.Ensaio):
        def aprovado(self):
            return self.valor == 1

    assert EnsaioExato("teste", 1).laudo() == "teste: 1.00 -> APROVADO"
