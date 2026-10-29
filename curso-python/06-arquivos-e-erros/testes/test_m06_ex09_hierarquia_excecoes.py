import pytest

from _curso import carregar

ex = carregar(__file__, "ex09_hierarquia_excecoes")

SPECS = {
    "123456": {"espessura": (22.5, 27.5), "cof": (0.15, 0.30)},
    "654321": {"espessura": (45.0, 55.0)},
}


def test_erro_de_qualidade_e_filha_de_exception():
    assert issubclass(ex.ErroDeQualidade, Exception)


@pytest.mark.parametrize("nome", ["EspecificacaoAusente", "ValorForaDaTolerancia"])
def test_filhas_de_erro_de_qualidade(nome):
    classe = getattr(ex, nome)
    assert issubclass(classe, ex.ErroDeQualidade), f"{nome} deve herdar de ErroDeQualidade"


def test_filhas_sao_tipos_diferentes():
    assert not issubclass(ex.EspecificacaoAusente, ex.ValorForaDaTolerancia)
    assert not issubclass(ex.ValorForaDaTolerancia, ex.EspecificacaoAusente)


@pytest.mark.parametrize(
    ("op", "ensaio", "valor"),
    [("123456", "espessura", 25.0), ("123456", "cof", 0.15), ("654321", "espessura", 55.0)],
)
def test_medicao_ok(op, ensaio, valor):
    assert ex.verificar_medicao(op, ensaio, valor, SPECS) == "OK"


def test_op_sem_especificacao():
    with pytest.raises(ex.EspecificacaoAusente, match="OP 999999 sem especificação"):
        ex.verificar_medicao("999999", "espessura", 25.0, SPECS)


def test_ensaio_sem_limite():
    with pytest.raises(ex.EspecificacaoAusente, match="OP 654321 sem limite para cof"):
        ex.verificar_medicao("654321", "cof", 0.2, SPECS)


def test_valor_fora():
    with pytest.raises(ex.ValorForaDaTolerancia, match=r"OP 123456: cof = 0\.35 fora de"):
        ex.verificar_medicao("123456", "cof", 0.35, SPECS)


def test_resumo_conta_aprovadas_e_junta_problemas():
    medicoes = [
        ("123456", "espessura", 25.0),
        ("123456", "cof", 0.35),
        ("999999", "espessura", 25.0),
        ("654321", "espessura", 50.0),
    ]
    resumo = ex.resumir_conferencia(medicoes, SPECS)
    assert resumo["aprovadas"] == 2
    assert len(resumo["problemas"]) == 2
    assert resumo["problemas"][1] == "OP 999999 sem especificação"


def test_resumo_vazio():
    assert ex.resumir_conferencia([], SPECS) == {"aprovadas": 0, "problemas": []}


def test_resumo_nao_esconde_bugs():
    with pytest.raises(TypeError):
        # valor None não é um problema de qualidade: é bug de quem chamou.
        ex.resumir_conferencia([("123456", "espessura", None)], SPECS)
