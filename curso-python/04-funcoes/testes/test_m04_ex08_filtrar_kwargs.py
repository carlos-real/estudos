from _curso import carregar

ex = carregar(__file__, "ex08_filtrar_kwargs")

TABELA = [
    {"op": "OP-1", "linha": "A", "status": "aprovado", "turno": 1},
    {"op": "OP-2", "linha": "B", "status": "aprovado", "turno": 2},
    {"op": "OP-3", "linha": "A", "status": "reprovado", "turno": 2},
    {"op": "OP-4", "linha": "A", "status": "aprovado"},
]


def test_criar_amostra_com_medicoes_nomeadas():
    amostra = ex.criar_amostra("OP-4512", " a", espessura=50.2, cof=0.22)
    assert amostra == {"op": "OP-4512", "linha": "A", "espessura": 50.2, "cof": 0.22}
    assert list(amostra) == ["op", "linha", "espessura", "cof"]


def test_criar_amostra_sem_medicoes():
    assert ex.criar_amostra("OP-1", "b") == {"op": "OP-1", "linha": "B"}


def test_criar_amostra_aceita_qualquer_nome_de_medicao():
    amostra = ex.criar_amostra("OP-2", "C", gramatura=46.1, tracao=31.5, selagem=2.8)
    assert amostra["tracao"] == 31.5
    assert amostra["selagem"] == 2.8


def test_filtrar_por_um_criterio():
    assert [r["op"] for r in ex.filtrar_registros(TABELA, linha="A")] == [
        "OP-1",
        "OP-3",
        "OP-4",
    ]


def test_filtrar_por_varios_criterios():
    resultado = ex.filtrar_registros(TABELA, linha="A", status="aprovado")
    assert [r["op"] for r in resultado] == ["OP-1", "OP-4"]


def test_coluna_ausente_nao_passa_no_filtro():
    resultado = ex.filtrar_registros(TABELA, turno=2, status="aprovado")
    assert [r["op"] for r in resultado] == ["OP-2"]


def test_sem_criterios_devolve_todos_em_lista_nova():
    resultado = ex.filtrar_registros(TABELA)
    assert resultado == TABELA
    assert resultado is not TABELA, "Devolva uma lista nova, mesmo sem critérios."


def test_nenhum_registro_atende():
    assert ex.filtrar_registros(TABELA, linha="Z") == []
