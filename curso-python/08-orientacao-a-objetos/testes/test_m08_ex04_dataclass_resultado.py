import dataclasses

import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_dataclass_resultado")


def test_e_uma_dataclass_com_os_campos_na_ordem():
    r = ex.ResultadoEnsaio("espessura", 25.3, "µm")
    assert dataclasses.is_dataclass(r), "Use o decorador @dataclass"
    nomes = [campo.name for campo in dataclasses.fields(r)]
    assert nomes == ["ensaio", "valor", "unidade", "aprovado"]


def test_valores_padrao():
    r = ex.ResultadoEnsaio("cof", 0.25)
    assert r.unidade == ""
    assert r.aprovado is True


def test_repr_gerado():
    r = ex.ResultadoEnsaio("cof", 0.32, aprovado=False)
    assert repr(r) == "ResultadoEnsaio(ensaio='cof', valor=0.32, unidade='', aprovado=False)"


def test_igualdade_por_valor():
    assert ex.ResultadoEnsaio("cof", 0.32) == ex.ResultadoEnsaio("cof", 0.32)
    assert ex.ResultadoEnsaio("cof", 0.32) != ex.ResultadoEnsaio("cof", 0.33)


@pytest.mark.parametrize(
    ("args", "kwargs", "esperado"),
    [
        (("espessura", 25.3, "µm"), {}, "espessura: 25.30 µm (aprovado)"),
        (("cof", 0.32), {"aprovado": False}, "cof: 0.32 (reprovado)"),
        (("tração", 31), {"unidade": "MPa"}, "tração: 31.00 MPa (aprovado)"),
    ],
)
def test_rotulo(args, kwargs, esperado):
    assert ex.ResultadoEnsaio(*args, **kwargs).rotulo() == esperado
