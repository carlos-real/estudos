from _curso import carregar

ex = carregar(__file__, "ex09_relatorio_no_terminal")


def test_relatorio_completo(capsys):
    ex.imprimir_relatorio([("12345", 25.4, True), ("12346", 27.1, False)])
    saida = capsys.readouterr().out
    assert saida == (
        "OP | VALOR | SITUAÇÃO\n12345 | 25,40 | OK\n12346 | 27,10 | FORA\n"
        "Total: 2 amostra(s), 1 fora\n"
    )


def test_valor_com_ponto_de_milhar(capsys):
    ex.imprimir_relatorio([("9", 1250.5, True)])
    linhas = capsys.readouterr().out.splitlines()
    assert linhas[1] == "9 | 1.250,50 | OK", "1250.5 deve aparecer como 1.250,50"


def test_valor_inteiro_ganha_duas_casas(capsys):
    ex.imprimir_relatorio([("7", 25, False)])
    linhas = capsys.readouterr().out.splitlines()
    assert linhas[1] == "7 | 25,00 | FORA"


def test_total_conta_quantos_estao_fora(capsys):
    resultados = [("1", 20.0, False), ("2", 20.0, True), ("3", 20.0, False)]
    ex.imprimir_relatorio(resultados)
    linhas = capsys.readouterr().out.splitlines()
    assert len(linhas) == 5, "cabeçalho + 3 linhas + total"
    assert linhas[-1] == "Total: 3 amostra(s), 2 fora"


def test_lista_vazia(capsys):
    ex.imprimir_relatorio([])
    assert capsys.readouterr().out == "Nenhuma amostra.\n"


def test_nao_devolve_nada(capsys):
    assert ex.imprimir_relatorio([("1", 20.0, True)]) is None
    assert capsys.readouterr().out != "", "a função precisa imprimir o relatório"
