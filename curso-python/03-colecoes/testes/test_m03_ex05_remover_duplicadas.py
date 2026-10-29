from _curso import carregar

ex = carregar(__file__, "ex05_remover_duplicadas")


def test_remove_lotes_repetidos_mantendo_a_ordem():
    lidos = ["L-101", "L-102", "L-101", "L-103", "L-102"]
    assert ex.remover_duplicadas(lidos) == ["L-101", "L-102", "L-103"]


def test_ordem_da_primeira_ocorrencia_nao_e_ordem_alfabetica():
    resultado = ex.remover_duplicadas(["L-300", "L-100", "L-300", "L-200"])
    assert resultado == ["L-300", "L-100", "L-200"], (
        "A ordem deve ser a da primeira leitura, não a alfabética nem a de um set."
    )


def test_lista_sem_repetidos_fica_igual():
    assert ex.remover_duplicadas(["A", "B", "C"]) == ["A", "B", "C"]


def test_todos_iguais():
    assert ex.remover_duplicadas(["L-1", "L-1", "L-1"]) == ["L-1"]


def test_lista_vazia():
    assert ex.remover_duplicadas([]) == []


def test_nao_modifica_a_lista_original():
    lidos = ["L-1", "L-2", "L-1"]
    resultado = ex.remover_duplicadas(lidos)
    assert lidos == ["L-1", "L-2", "L-1"], "A lista recebida não pode ser alterada."
    assert resultado is not lidos
