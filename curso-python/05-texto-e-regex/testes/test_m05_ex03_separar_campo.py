from _curso import carregar

ex = carregar(__file__, "ex03_separar_campo")


def test_rotulo_e_valor():
    assert ex.separar_campo("Espessura (µm): 25,0") == ("Espessura (µm)", "25,0")


def test_divide_so_no_primeiro_dois_pontos():
    assert ex.separar_campo("  Horário da coleta :  14:30 ") == (
        "Horário da coleta",
        "14:30",
    ), "O valor pode ter ':' dentro. Divida só no primeiro."


def test_linha_sem_dois_pontos():
    assert ex.separar_campo("  Observações gerais ") == ("Observações gerais", "")


def test_valor_vazio():
    assert ex.separar_campo("COF:") == ("COF", "")


def test_devolve_tupla():
    resultado = ex.separar_campo("NF: 98765")
    assert isinstance(resultado, tuple), "Devolva uma tupla (rótulo, valor)."
    assert resultado == ("NF", "98765")
