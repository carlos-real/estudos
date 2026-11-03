import pytest
from pydantic import ValidationError

from _curso import carregar

ex = carregar(__file__, "ex05_modelos_pydantic")

VALIDA = {"op": "123456", "linha": "A", "ensaio": "espessura", "valor": 20.4}


def test_cria_medicao_valida():
    m = ex.Medicao(**VALIDA)
    assert (m.op, m.linha, m.ensaio, m.valor) == ("123456", "A", "espessura", 20.4)


def test_valores_padrao():
    m = ex.Medicao(**VALIDA)
    assert m.unidade == "µm"
    assert m.observacao is None


def test_converte_texto_em_float():
    m = ex.Medicao(**{**VALIDA, "valor": "0.27"})
    assert m.valor == pytest.approx(0.27)
    assert isinstance(m.valor, float)


def test_model_dump():
    m = ex.Medicao(**{**VALIDA, "unidade": "g/m²", "observacao": "COF: liberado"})
    assert m.model_dump() == {**VALIDA, "unidade": "g/m²", "observacao": "COF: liberado"}


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("op", "12345"),
        ("op", "1234567"),
        ("op", "12a456"),
        ("linha", "E"),
        ("linha", "a"),
        ("ensaio", "x"),
        ("valor", 0),
        ("valor", -3.5),
        ("valor", "abc"),
    ],
)
def test_dados_invalidos_levantam_validation_error(campo, valor):
    with pytest.raises(ValidationError):
        ex.Medicao(**{**VALIDA, campo: valor})


@pytest.mark.parametrize("faltando", ["op", "linha", "ensaio", "valor"])
def test_campos_obrigatorios(faltando):
    dados = {k: v for k, v in VALIDA.items() if k != faltando}
    with pytest.raises(ValidationError):
        ex.Medicao(**dados)


def test_resumo():
    assert ex.resumo(ex.Medicao(**VALIDA)) == "OP 123456 | linha A | espessura: 20.4 µm"
    m = ex.Medicao(op="124001", linha="C", ensaio="tracao", valor=31, unidade="MPa")
    assert ex.resumo(m) == "OP 124001 | linha C | tracao: 31.0 MPa"
