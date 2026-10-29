import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_fila_emissao")


@pytest.fixture
def especificacoes():
    T = ex.Tolerancia
    return {
        "PADRAO-A": ex.Especificacao(
            "PADRAO-A",
            linha="A",
            tolerancias={
                "espessura": T("espessura", "nominal", percentual=10.0),
                "cof": T("cof", "fixa", minimo=0.15, maximo=0.35),
                "selagem": T("selagem", "fixa", minimo=8.0),
            },
        ),
        "PADRAO-C": ex.Especificacao(
            "PADRAO-C",
            linha="C",
            tolerancias={
                "cof": T("cof", "fixa", minimo=0.10, maximo=0.30),
                "selagem": T("selagem", "fixa", minimo=10.0),
            },
        ),
        "ESP-0412": ex.Especificacao(
            "ESP-0412", tolerancias={"cof": T("cof", "fixa", minimo=0.18, maximo=0.25)}
        ),
    }


def medicao(**mudancas):
    dados = {
        "op": "24518",
        "aba": "Linha A",
        "linha": "A",
        "valores": {"espessura": 41.2, "cof": 0.22, "selagem": 9.8},
        "nominais": {"espessura": 40.0},
        "observacao": "COF: liberado",
    }
    dados.update(mudancas)
    return ex.Medicao(**dados)


def pedido(op="24518", nf="123456", peso=1250.5):
    return ex.Pedido(op=op, nf=nf, peso_kg=peso)


def test_aprovada_e_liberada_vai_para_a_fila(especificacoes):
    fila, bloqueados = ex.montar_fila([pedido()], [medicao()], especificacoes)
    assert bloqueados == []
    assert len(fila) == 1
    item = fila[0]
    assert isinstance(item, ex.ItemFila)
    assert (item.op, item.nf, item.peso_kg) == ("24518", "123456", 1250.5)
    assert (item.situacao, item.especificacao, item.motivos) == ("emitir", "PADRAO-A", [])


def test_reprovada_e_sem_liberacao_juntam_os_motivos(especificacoes):
    m = medicao(
        valores={"espessura": 44.8, "cof": 0.22, "selagem": 9.8},
        observacao="COF: não liberado",
    )
    fila, bloqueados = ex.montar_fila([pedido()], [m], especificacoes)
    assert fila == []
    item = bloqueados[0]
    assert (item.situacao, item.especificacao) == ("bloqueado", "PADRAO-A")
    assert item.motivos == ["espessura 44.8 fora de 40 ± 10% (36 a 44)", ex.SEM_LIBERACAO]


def test_op_nao_encontrada(especificacoes):
    _, bloqueados = ex.montar_fila([pedido(op="99999")], [medicao()], especificacoes)
    assert bloqueados[0].motivos == ["OP não encontrada na planilha"]
    assert bloqueados[0].especificacao == ""


def test_op_repetida_na_planilha(especificacoes):
    repetidas = [medicao(), medicao(aba="Linha C", linha="C")]
    _, bloqueados = ex.montar_fila([pedido()], repetidas, especificacoes)
    assert bloqueados[0].motivos == ["OP aparece 2 vezes na planilha"]


def test_linha_divergente_para_antes_da_validacao(especificacoes):
    m = medicao(linha="C", observacao="")
    _, bloqueados = ex.montar_fila([pedido()], [m], especificacoes)
    assert bloqueados[0].motivos == ["linha informada C diferente da aba Linha A"], (
        "Linha divergente para a triagem: não valida nem confere liberação."
    )


def test_especificacao_desconhecida(especificacoes):
    m = medicao(especificacao="ESP-9999")
    _, bloqueados = ex.montar_fila([pedido()], [m], especificacoes)
    assert bloqueados[0].motivos == ["especificação 'ESP-9999' não cadastrada"]


def test_especificacao_do_cliente_e_aplicada(especificacoes):
    m = medicao(
        op="24542",
        aba="Linha C",
        linha="C",
        especificacao="ESP-0412",
        valores={"cof": 0.27, "selagem": 12.9},
    )
    _, bloqueados = ex.montar_fila([pedido(op="24542")], [m], especificacoes)
    assert bloqueados[0].especificacao == "ESP-0412"
    assert bloqueados[0].motivos == ["cof 0.27 acima do máximo 0.25"]


def test_ordem_dos_pedidos_e_preservada(especificacoes):
    medicoes = [medicao(op="1"), medicao(op="2", observacao=""), medicao(op="3")]
    pedidos = [pedido("3"), pedido("2"), pedido("4"), pedido("1")]
    fila, bloqueados = ex.montar_fila(pedidos, medicoes, especificacoes)
    assert [i.op for i in fila] == ["3", "1"]
    assert [i.op for i in bloqueados] == ["2", "4"]
