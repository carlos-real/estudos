import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_validar_op")


@pytest.fixture
def padrao_a():
    return ex.Especificacao(
        "PADRAO-A",
        linha="A",
        tolerancias={
            "espessura": ex.Tolerancia("espessura", "nominal", percentual=10.0),
            "cof": ex.Tolerancia("cof", "fixa", minimo=0.15, maximo=0.35),
            "selagem": ex.Tolerancia("selagem", "fixa", minimo=8.0),
        },
    )


def medicao(**mudancas):
    dados = {
        "op": "24518",
        "aba": "Linha A",
        "linha": "A",
        "valores": {"espessura": 41.2, "cof": 0.22, "selagem": 9.8},
        "nominais": {"espessura": 40.0},
    }
    dados.update(mudancas)
    return ex.Medicao(**dados)


def test_op_aprovada(padrao_a):
    resultado = ex.validar_medicao(medicao(), padrao_a)
    assert isinstance(resultado, ex.ResultadoValidacao)
    assert (resultado.op, resultado.especificacao, resultado.motivos) == (
        "24518",
        "PADRAO-A",
        [],
    )
    assert resultado.aprovado


def test_reprovada_na_nominal(padrao_a):
    m = medicao(op="24519", valores={"espessura": 44.8, "cof": 0.24, "selagem": 9.1})
    resultado = ex.validar_medicao(m, padrao_a)
    assert resultado.motivos == ["espessura 44.8 fora de 40 ± 10% (36 a 44)"]
    assert resultado.op == "24519"


def test_junta_todos_os_motivos_na_ordem_da_especificacao(padrao_a):
    m = medicao(valores={"espessura": 39.5, "cof": 0.38, "selagem": 7.6})
    assert ex.validar_medicao(m, padrao_a).motivos == [
        "cof 0.38 acima do máximo 0.35",
        "selagem 7.6 abaixo do mínimo 8",
    ]


def test_falta_de_valor_e_de_nominal_viram_motivo(padrao_a):
    m = medicao(valores={"espessura": 41.0, "cof": 0.22}, nominais={})
    assert ex.validar_medicao(m, padrao_a).motivos == [
        "espessura sem valor nominal",
        "selagem sem valor medido",
    ]


def test_caracteristica_nao_exigida_e_ignorada(padrao_a):
    m = medicao(valores={"espessura": 41.2, "cof": 0.22, "selagem": 9.8, "tracao": 1.0})
    assert ex.validar_medicao(m, padrao_a).motivos == []


def test_especificacao_sem_tolerancias_aprova():
    vazia = ex.Especificacao("ESP-0700")
    resultado = ex.validar_medicao(medicao(valores={}), vazia)
    assert resultado.motivos == []
    assert resultado.especificacao == "ESP-0700"
