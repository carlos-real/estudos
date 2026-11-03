import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_corrigir_plano_robo")


def pedido(**mudancas):
    base = {"op": "123456", "nf": "98765", "peso_kg": 1250.5, "linha": "B"}
    base.update(mudancas)
    return base


def test_plano_completo_em_ensaio():
    assert ex.planejar_certificado(pedido()) == [
        ("preencher", "OP", "123456"),
        ("preencher", "NF", "98765"),
        ("preencher", "Peso (kg)", "1.250,50"),
        ("selecionar", "Linha", "B"),
        ("print", "antes_de_confirmar_123456", ""),
        ("clicar", "Cancelar", ""),
    ]


def test_ensaio_nunca_confirma():
    acoes = ex.planejar_certificado(pedido(), ensaio=True)
    assert ("clicar", "Confirmar", "") not in acoes, "PERIGO: o ensaio está confirmando!"
    assert acoes[-1] == ("clicar", "Cancelar", "")


def test_modo_real_confirma_no_final():
    acoes = ex.planejar_certificado(pedido(), ensaio=False)
    assert acoes[-1] == ("clicar", "Confirmar", "")
    assert ("clicar", "Cancelar", "") not in acoes


def test_chamadas_seguidas_nao_se_misturam():
    primeira = ex.planejar_certificado(pedido(op="111111"))
    segunda = ex.planejar_certificado(pedido(op="222222"))
    assert len(primeira) == 6
    assert len(segunda) == 6, "A lista de ações está sendo reaproveitada entre chamadas"
    assert ("preencher", "OP", "111111") not in segunda


@pytest.mark.parametrize(
    ("peso", "texto"),
    [(1250.5, "1.250,50"), (980.25, "980,25"), (1234567.891, "1.234.567,89"), (0.5, "0,50")],
)
def test_peso_no_formato_brasileiro(peso, texto):
    acoes = ex.planejar_certificado(pedido(peso_kg=peso))
    assert ("preencher", "Peso (kg)", texto) in acoes


def test_observacao_quando_existe():
    acoes = ex.planejar_certificado(pedido(observacao="COF: liberado"))
    assert acoes[4] == ("preencher", "Observação", "COF: liberado")
    assert len(acoes) == 7


def test_observacao_vazia_nao_entra():
    acoes = ex.planejar_certificado(pedido(observacao=""))
    assert all(alvo != "Observação" for _, alvo, _ in acoes)


@pytest.mark.parametrize("op", ["12345", "1234567", "12a456", "", "OP1234"])
def test_op_invalida(op):
    with pytest.raises(ValueError):
        ex.planejar_certificado(pedido(op=op))


@pytest.mark.parametrize("peso", [0, -10.5])
def test_peso_invalido(peso):
    with pytest.raises(ValueError):
        ex.planejar_certificado(pedido(peso_kg=peso))
