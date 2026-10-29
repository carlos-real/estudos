from collections import Counter

import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_contar_reprovacoes")


def ensaio(op, linha, resultado, nome="espessura"):
    return {"op": op, "linha": linha, "ensaio": nome, "resultado": resultado}


SEMANA = [
    ensaio("OP1", "A", "aprovado"),
    ensaio("OP2", "B", "reprovado", "cof"),
    ensaio("OP3", "C", "reprovado"),
    ensaio("OP3", "C", "Reprovado", "gramatura"),
    ensaio("OP4", "D", "aprovado"),
    ensaio("OP5", "C", "REPROVADO"),
    ensaio("OP6", "B", "aprovado"),
    ensaio("OP7", "A", "reprovado"),
    ensaio("OP8", "B", "reprovado"),
]


def test_contar_reprovacoes_da_semana():
    assert ex.contar_reprovacoes(SEMANA) == {"C": 3, "B": 2, "A": 1}


def test_contar_reprovacoes_devolve_counter():
    resultado = ex.contar_reprovacoes(SEMANA)
    assert isinstance(resultado, Counter), "Devolva um collections.Counter"
    assert resultado["D"] == 0


def test_contar_reprovacoes_sem_reprovacao():
    resultado = ex.contar_reprovacoes([ensaio("OP1", "A", "aprovado")])
    assert isinstance(resultado, Counter)
    assert len(resultado) == 0


def test_contar_reprovacoes_lista_vazia():
    resultado = ex.contar_reprovacoes([])
    assert isinstance(resultado, Counter)
    assert resultado == Counter()


@pytest.mark.parametrize(
    ("n", "esperado"),
    [(1, [("C", 3)]), (2, [("C", 3), ("B", 2)]), (5, [("C", 3), ("B", 2), ("A", 1)])],
)
def test_piores_linhas(n, esperado):
    assert ex.piores_linhas(SEMANA, n) == esperado


def test_piores_linhas_padrao_sao_duas():
    assert ex.piores_linhas(SEMANA) == [("C", 3), ("B", 2)]


def test_piores_linhas_empate_respeita_ordem_de_aparicao():
    dados = [ensaio("OP1", "D", "reprovado"), ensaio("OP2", "A", "reprovado")]
    assert ex.piores_linhas(dados, 2) == [("D", 1), ("A", 1)]


def test_taxa_reprovacao_inclui_linhas_sem_reprovacao():
    assert ex.taxa_reprovacao(SEMANA) == {
        "A": pytest.approx(50.0),
        "B": pytest.approx(66.7),
        "C": pytest.approx(100.0),
        "D": pytest.approx(0.0),
    }
