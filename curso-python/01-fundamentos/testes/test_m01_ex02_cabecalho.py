from _curso import carregar

ex = carregar(__file__, "ex02_cabecalho")


def test_cabecalho_de_largura_20(capsys):
    ex.imprimir_cabecalho("laudo de espessura", 20)
    saida = capsys.readouterr().out
    esperado = "====================\nLAUDO DE ESPESSURA\n====================\n"
    assert saida == esperado, f"Saída impressa:\n{saida}\nSaída esperada:\n{esperado}"


def test_titulo_com_acento_fica_em_maiusculas(capsys):
    ex.imprimir_cabecalho("relatório de selagem", 25)
    linhas = capsys.readouterr().out.splitlines()
    assert linhas == ["=" * 25, "RELATÓRIO DE SELAGEM", "=" * 25]


def test_largura_menor_que_o_titulo(capsys):
    ex.imprimir_cabecalho("certificado de qualidade", 10)
    linhas = capsys.readouterr().out.splitlines()
    assert linhas == ["==========", "CERTIFICADO DE QUALIDADE", "=========="]


def test_funcao_imprime_e_nao_devolve_nada(capsys):
    resultado = ex.imprimir_cabecalho("cof", 5)
    assert capsys.readouterr().out != "", "A função precisa IMPRIMIR o cabeçalho."
    assert resultado is None, "Esta função só imprime; não precisa de return."
