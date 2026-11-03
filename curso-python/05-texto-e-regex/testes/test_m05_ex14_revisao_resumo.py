from _curso import carregar

ex = carregar(__file__, "ex14_revisao_resumo")

PEDIDOS = [
    {"op": "123457", "nf": "98766", "peso_kg": 980.0},
    {"op": "123456", "nf": "98765", "peso_kg": 1250.5},
]


def test_resumo_completo():
    esperado = (
        "OP 123456 | NF 000.098.765 |   1.250,50 kg\n"
        "OP 123457 | NF 000.098.766 |     980,00 kg\n"
        "Total: 2 pedidos           |   2.230,50 kg"
    )
    assert ex.montar_resumo(PEDIDOS) == esperado


def test_ordena_por_op_sem_alterar_a_lista_original():
    copia = [dict(p) for p in PEDIDOS]
    linhas = ex.montar_resumo(PEDIDOS).split("\n")
    assert linhas[0].startswith("OP 123456") and linhas[1].startswith("OP 123457")
    assert PEDIDOS == copia, "Não altere a lista recebida (use sorted, não .sort())."


def test_singular_com_um_pedido():
    resumo = ex.montar_resumo([{"op": "000001", "nf": "1", "peso_kg": 12.5}])
    assert resumo == (
        "OP 000001 | NF 000.000.001 |      12,50 kg\n"
        "Total: 1 pedido            |      12,50 kg"
    )


def test_numero_grande_e_linhas_alinhadas():
    pedidos = [
        {"op": "200000", "nf": "123456789", "peso_kg": 1234567.891},
        {"op": "100000", "nf": "42", "peso_kg": 0.5},
    ]
    linhas = ex.montar_resumo(pedidos).split("\n")
    assert linhas == [
        "OP 100000 | NF 000.000.042 |       0,50 kg",
        "OP 200000 | NF 123.456.789 | 1.234.567,89 kg",
        "Total: 2 pedidos           | 1.234.568,39 kg",
    ]


def test_sem_quebra_de_linha_no_fim():
    assert not ex.montar_resumo(PEDIDOS).endswith("\n")


def test_lista_vazia():
    assert ex.montar_resumo([]) == "Nenhum pedido encontrado."
