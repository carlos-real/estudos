from _curso import carregar

ex = carregar(__file__, "ex07_ordenar_com_key")


def test_mais_proxima_do_nominal():
    assert ex.mais_proxima_do_nominal([50.6, 49.8, 51.0], 50.0) == 49.8


def test_mais_proxima_em_empate_fica_com_a_primeira():
    assert ex.mais_proxima_do_nominal([52.0, 48.0, 51.0], 50.0) == 51.0
    assert ex.mais_proxima_do_nominal([52.0, 48.0], 50.0) == 52.0


def test_mais_proxima_de_lista_vazia_e_none():
    assert ex.mais_proxima_do_nominal([], 50.0) is None


def test_ordenar_por_desvio():
    assert ex.ordenar_por_desvio([53.0, 50.5, 47.0, 49.0], 50.0) == [50.5, 49.0, 53.0, 47.0]


def test_ordenar_por_desvio_empate_mantem_ordem_original():
    assert ex.ordenar_por_desvio([47.0, 53.0, 50.0], 50.0) == [50.0, 47.0, 53.0]


def test_ordenar_por_desvio_nao_altera_a_original():
    medicoes = [53.0, 50.5]
    resultado = ex.ordenar_por_desvio(medicoes, 50.0)
    assert medicoes == [53.0, 50.5], "Use sorted (lista nova), não .sort()."
    assert resultado == [50.5, 53.0]


def test_ordenar_palavras_por_tamanho_e_alfabetica():
    resultado = ex.ordenar_palavras(["Selagem", "cof", "tração", "Gel"])
    assert resultado == ["cof", "Gel", "tração", "Selagem"]


def test_ordenar_palavras_sem_diferenciar_maiusculas():
    assert ex.ordenar_palavras(["Bb", "ab", "Aa"]) == ["Aa", "ab", "Bb"], (
        "No empate de tamanho, compare em minúsculas: 'Aa' < 'ab' < 'Bb'."
    )


def test_ordenar_palavras_vazia():
    assert ex.ordenar_palavras([]) == []
