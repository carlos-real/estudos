import copy

import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_juntar_tabelas")

PEDIDOS = [
    {"op": "op-4512", "nf": "123", "peso_kg": 500.0},
    {"op": " OP 4513 ", "nf": "124", "peso_kg": 320.5},
    {"op": "OP-4514", "nf": "125", "peso_kg": 210.25},
    {"op": "OP-4599", "nf": "126", "peso_kg": 80.5},
    {"op": "OP-4515", "nf": "127", "peso_kg": 99.95},
]
RESULTADOS = [
    {"op": "OP-4512", "linha": "A", "status": " Aprovado"},
    {"op": "OP-4513", "linha": "B", "status": "REPROVADO"},
    {"op": "op-4514", "linha": "C", "status": "aprovado "},
    {"op": "OP-4515", "linha": "D", "status": "reprovado"},
    {"op": "OP-4515", "linha": "D", "status": "Aprovado"},
]


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [(" op 4512 ", "OP-4512"), ("op-4512", "OP-4512"), ("OP-4512", "OP-4512")],
)
def test_normalizar_op(texto, esperado):
    assert ex.normalizar_op(texto) == esperado


def test_indexar_por_op_normaliza_e_fica_com_o_ultimo():
    indice = ex.indexar_por_op(RESULTADOS)
    assert set(indice) == {"OP-4512", "OP-4513", "OP-4514", "OP-4515"}
    assert indice["OP-4514"]["linha"] == "C"
    assert indice["OP-4515"]["status"] == "Aprovado", "OP repetida: vale o ÚLTIMO resultado."


def test_juntar_preenche_linha_e_status():
    juntados = ex.juntar(PEDIDOS, RESULTADOS)
    assert juntados[0] == {
        "op": "OP-4512",
        "nf": "123",
        "peso_kg": 500.0,
        "linha": "A",
        "status": "aprovado",
    }
    assert [j["status"] for j in juntados] == [
        "aprovado",
        "reprovado",
        "aprovado",
        "sem resultado",
        "aprovado",
    ]


def test_juntar_pedido_sem_resultado():
    juntados = ex.juntar(PEDIDOS, RESULTADOS)
    assert juntados[3] == {
        "op": "OP-4599",
        "nf": "126",
        "peso_kg": 80.5,
        "linha": None,
        "status": "sem resultado",
    }


def test_juntar_mantem_chaves_extras_do_pedido():
    pedidos = [{"op": "OP-4512", "nf": "1", "peso_kg": 1.0, "cliente": "Alfa"}]
    juntado = ex.juntar(pedidos, RESULTADOS)[0]
    assert juntado["cliente"] == "Alfa"


def test_juntar_nao_altera_as_tabelas_originais():
    pedidos = copy.deepcopy(PEDIDOS)
    resultados = copy.deepcopy(RESULTADOS)
    ex.juntar(pedidos, resultados)
    assert pedidos == PEDIDOS, "Os pedidos originais foram alterados: crie dicionários novos."
    assert resultados == RESULTADOS


def test_resumo_expedicao():
    resumo = ex.resumo_expedicao(ex.juntar(PEDIDOS, RESULTADOS))
    assert resumo["emitir"] == ["OP-4512", "OP-4514", "OP-4515"]
    assert resumo["bloqueadas"] == ["OP-4513"]
    assert resumo["sem_resultado"] == ["OP-4599"]
    assert resumo["peso_emitir_kg"] == pytest.approx(810.2)


def test_resumo_de_lista_vazia():
    assert ex.resumo_expedicao([]) == {
        "emitir": [],
        "bloqueadas": [],
        "sem_resultado": [],
        "peso_emitir_kg": 0.0,
    }


def test_status_desconhecido_vai_para_bloqueadas():
    juntados = [{"op": "OP-1", "peso_kg": 10.0, "status": "em análise"}]
    assert ex.resumo_expedicao(juntados)["bloqueadas"] == ["OP-1"]
