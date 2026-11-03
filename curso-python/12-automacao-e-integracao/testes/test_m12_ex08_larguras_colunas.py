from _curso import carregar

ex = carregar(__file__, "ex08_larguras_colunas")


def test_maior_texto_mais_folga():
    linhas = [["OP", "Ensaio"], ["123456", "Espessura"]]
    assert ex.calcular_larguras(linhas) == [8, 11]


def test_numeros_contam_pelo_texto():
    linhas = [["Valor", "Peso (kg)"], [1250.75, 98765432.125]]
    assert ex.calcular_larguras(linhas) == [9, 14]


def test_respeita_o_minimo():
    assert ex.calcular_larguras([["A"], ["B"]]) == [8]
    assert ex.calcular_larguras([["A"]], minimo=3) == [3]


def test_respeita_o_maximo():
    linhas = [["Observação"], ["x" * 80]]
    assert ex.calcular_larguras(linhas) == [50]
    assert ex.calcular_larguras(linhas, maximo=30) == [30]


def test_none_conta_como_vazio():
    linhas = [["OP", None], [None, None]]
    assert ex.calcular_larguras(linhas, minimo=0) == [4, 2]


def test_linhas_de_tamanhos_diferentes():
    linhas = [["OP"], ["123456", "Tração longitudinal"], []]
    assert ex.calcular_larguras(linhas) == [8, 21]


def test_sem_linhas():
    assert ex.calcular_larguras([]) == []
