from validador_certificados.fila import SEM_LIBERACAO, montar_fila
from validador_certificados.modelos import Pedido


def pedido(op="24518", nf="123456"):
    return Pedido(op=op, nf=nf, peso_kg=1250.5)


def test_op_aprovada_e_liberada_vai_para_a_fila(especificacoes, nova_medicao):
    fila, bloqueados = montar_fila([pedido()], [nova_medicao()], especificacoes)
    assert bloqueados == []
    assert len(fila) == 1
    item = fila[0]
    assert (item.op, item.nf, item.situacao, item.especificacao) == (
        "24518",
        "123456",
        "emitir",
        "PADRAO-A",
    )


def test_reprovada_e_sem_liberacao_juntam_motivos(especificacoes, nova_medicao):
    medicao = nova_medicao(
        valores={"espessura": 44.8, "cof": 0.22, "selagem": 9.8}, observacao="COF: aguardando"
    )
    fila, bloqueados = montar_fila([pedido()], [medicao], especificacoes)
    assert fila == []
    assert bloqueados[0].motivos == [
        "espessura 44.8 fora de 40 ± 10% (36 a 44)",
        SEM_LIBERACAO,
    ]


def test_pendencias_de_dados(especificacoes, nova_medicao):
    medicoes = [
        nova_medicao(op="1"),
        nova_medicao(op="1", aba="Linha C", linha="C"),
        nova_medicao(op="2", linha="C"),
        nova_medicao(op="3", especificacao="ESP-9999"),
    ]
    pedidos = [pedido("1"), pedido("2"), pedido("3"), pedido("4")]
    fila, bloqueados = montar_fila(pedidos, medicoes, especificacoes)
    assert fila == []
    assert [b.motivos for b in bloqueados] == [
        ["OP aparece 2 vezes na planilha"],
        ["linha informada C diferente da aba Linha A"],
        ["especificação 'ESP-9999' não cadastrada"],
        ["OP não encontrada na planilha"],
    ]


def test_especificacao_do_cliente_e_mais_rigida(especificacoes, nova_medicao):
    medicao = nova_medicao(
        aba="Linha C",
        linha="C",
        especificacao="ESP-0412",
        valores={"espessura": 41.0, "cof": 0.27, "selagem": 13.0},
    )
    _, bloqueados = montar_fila([pedido()], [medicao], especificacoes)
    assert bloqueados[0].especificacao == "ESP-0412"
    assert bloqueados[0].motivos == ["cof 0.27 acima do máximo 0.25"]
