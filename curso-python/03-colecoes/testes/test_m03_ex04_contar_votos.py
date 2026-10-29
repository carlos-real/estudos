from _curso import carregar

ex = carregar(__file__, "ex04_contar_votos")


def test_conta_votos_simples():
    assert ex.contar_votos(["lasanha", "feijoada", "lasanha"]) == {"lasanha": 2, "feijoada": 1}


def test_normaliza_maiusculas_e_espacos():
    contagem = ex.contar_votos(["Feijoada", "feijoada ", " FEIJOADA", "Lasanha"])
    assert contagem == {"feijoada": 3, "lasanha": 1}, (
        "Votos iguais escritos de jeitos diferentes devem ser somados (strip + lower)."
    )


def test_ignora_votos_vazios():
    assert ex.contar_votos(["", "   ", "pizza"]) == {"pizza": 1}


def test_ordem_das_chaves_e_a_do_primeiro_voto():
    contagem = ex.contar_votos(["strogonoff", "Feijoada", "lasanha", "feijoada"])
    assert list(contagem) == ["strogonoff", "feijoada", "lasanha"]


def test_lista_vazia_devolve_dicionario_vazio():
    assert ex.contar_votos([]) == {}


def test_vencedor_e_o_mais_votado():
    assert ex.vencedor({"lasanha": 1, "feijoada": 3, "pizza": 2}) == "feijoada"


def test_empate_fica_com_o_primeiro():
    assert ex.vencedor({"pizza": 2, "lasanha": 2, "salada": 1}) == "pizza"


def test_vencedor_de_contagem_vazia_e_none():
    assert ex.vencedor({}) is None
