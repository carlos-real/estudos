from _curso import carregar

ex = carregar(__file__, "ex09_ranking_alunos")

NOTAS = {"Carla": 8.5, "Bruno": 9.0, "Ana": 8.5, "Davi": 4.0}


def test_ranking_da_maior_para_a_menor_nota():
    resultado = ex.ranking({"Ana": 7.0, "Bruno": 9.5, "Carla": 8.0})
    assert resultado == [("Bruno", 9.5), ("Carla", 8.0), ("Ana", 7.0)]


def test_empate_desempata_por_nome():
    assert ex.ranking(NOTAS) == [
        ("Bruno", 9.0),
        ("Ana", 8.5),
        ("Carla", 8.5),
        ("Davi", 4.0),
    ], "Notas iguais: o nome em ordem alfabética vem primeiro (Ana antes de Carla)."


def test_ranking_vazio():
    assert ex.ranking({}) == []


def test_ranking_nao_altera_o_dicionario():
    notas = {"Bia": 5.0, "Caio": 6.0}
    ex.ranking(notas)
    assert notas == {"Bia": 5.0, "Caio": 6.0}


def test_aprovados_em_ordem_alfabetica():
    assert ex.aprovados(NOTAS, 6.0) == ["Ana", "Bruno", "Carla"]


def test_nota_igual_a_media_aprova():
    assert ex.aprovados({"Ana": 6.0, "Bia": 5.9}, 6.0) == ["Ana"]


def test_ninguem_aprovado():
    assert ex.aprovados(NOTAS, 10.0) == []
