from _curso import carregar

ex = carregar(__file__, "ex13_revisao_tabela_limites")


def test_uma_linha_dois_nominais():
    resultado = ex.tabela_limites("A", [20, 25])
    esperado = "Linha A (±5%)\n  20.00 µm: 19.00 a 21.00\n  25.00 µm: 23.75 a 26.25\n"
    assert resultado == esperado, f"Devolvido:\n{resultado!r}\nEsperado:\n{esperado!r}"


def test_duas_linhas_com_minuscula_e_espaco():
    resultado = ex.tabela_limites("a c", [20])
    esperado = (
        "Linha A (±5%)\n  20.00 µm: 19.00 a 21.00\nLinha C (±8%)\n  20.00 µm: 18.40 a 21.60\n"
    )
    assert resultado == esperado, f"Devolvido:\n{resultado!r}\nEsperado:\n{esperado!r}"


def test_linha_desconhecida():
    assert ex.tabela_limites("X", [20, 25]) == "Linha X: sem tolerância cadastrada\n"


def test_mistura_conhecida_e_desconhecida():
    resultado = ex.tabela_limites("DZ", [25])
    esperado = (
        "Linha D (±10%)\n  25.00 µm: 22.50 a 27.50\nLinha Z: sem tolerância cadastrada\n"
    )
    assert resultado == esperado


def test_quantidade_de_linhas_do_texto():
    resultado = ex.tabela_limites("ABCD", [20, 25, 30])
    assert resultado.count("\n") == 16, "4 cabeçalhos + 4 x 3 linhas de limites = 16 linhas."
    assert resultado.endswith("\n")


def test_sem_linhas_devolve_texto_vazio():
    assert ex.tabela_limites("", [20, 25]) == ""
