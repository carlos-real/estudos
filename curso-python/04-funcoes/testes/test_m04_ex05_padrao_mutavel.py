from _curso import carregar

ex = carregar(__file__, "ex05_padrao_mutavel")


def test_sem_lista_cria_lista_com_o_defeito():
    assert ex.adicionar_defeito("Bolha") == ["bolha"]


def test_chamadas_sem_lista_nao_compartilham_a_mesma_lista():
    primeira = ex.adicionar_defeito("Bolha")
    segunda = ex.adicionar_defeito("Risco")
    assert segunda == ["risco"], (
        "A segunda chamada não pode 'lembrar' a primeira: é a armadilha do padrão mutável."
    )
    assert primeira == ["bolha"]
    assert primeira is not segunda


def test_normaliza_o_defeito():
    assert ex.adicionar_defeito("  GEL ") == ["gel"]


def test_acrescenta_na_lista_recebida_e_devolve_a_mesma():
    anotados = ["gel"]
    resultado = ex.adicionar_defeito(" Bolha ", anotados)
    assert resultado == ["gel", "bolha"]
    assert resultado is anotados, "Com lista informada, acrescente nela e devolva ela mesma."


def test_lista_vazia_informada_tambem_e_usada():
    vazia = []
    resultado = ex.adicionar_defeito("risco", vazia)
    assert vazia == ["risco"], "Use 'is None': uma lista vazia passada de propósito vale."
    assert resultado is vazia
