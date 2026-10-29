import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_laudo_decomposto")

LIMITES = (45.0, 55.0)


@pytest.mark.parametrize(
    ("nominal", "pct", "esperado"),
    [(50.0, 10.0, (45.0, 55.0)), (46.0, 5.0, (43.7, 48.3)), (20.0, 0.0, (20.0, 20.0))],
)
def test_calcular_limites(nominal, pct, esperado):
    assert ex.calcular_limites(nominal, pct) == esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(44.9, "abaixo"), (45.0, "ok"), (50.0, "ok"), (55.0, "ok"), (55.1, "acima")],
)
def test_classificar(valor, esperado):
    assert ex.classificar(valor, LIMITES) == esperado


def test_classificar_todas_mantem_a_ordem():
    assert ex.classificar_todas([50.2, 44.1, 56.3], LIMITES) == ["ok", "abaixo", "acima"]
    assert ex.classificar_todas([], LIMITES) == []


def test_contar_por_classe_sempre_tem_as_tres_chaves():
    assert ex.contar_por_classe(["ok", "ok", "acima"]) == {"abaixo": 0, "ok": 2, "acima": 1}
    assert ex.contar_por_classe([]) == {"abaixo": 0, "ok": 0, "acima": 0}


def test_contar_por_classe_na_ordem_abaixo_ok_acima():
    assert list(ex.contar_por_classe(["acima", "ok"])) == ["abaixo", "ok", "acima"]


def test_resumo_reprovado():
    medicoes = [50.2, 49.8, 44.1, 51.0, 50.5, 49.9]
    assert ex.resumo_lote("OP-4512", medicoes, 50.0, 10.0) == (
        "OP-4512 | 5/6 conformes (83.3%) | 1 abaixo, 0 acima | REPROVADO"
    )


def test_resumo_aprovado():
    assert ex.resumo_lote("OP-4514", [45.0, 55.0], 50.0, 10.0) == (
        "OP-4514 | 2/2 conformes (100.0%) | 0 abaixo, 0 acima | APROVADO"
    )


def test_resumo_com_gramatura_e_limite_arredondado():
    assert ex.resumo_lote("OP-7", [43.7, 48.3, 48.4], 46.0, 5.0) == (
        "OP-7 | 2/3 conformes (66.7%) | 0 abaixo, 1 acima | REPROVADO"
    )


def test_resumo_sem_medicoes():
    assert ex.resumo_lote("OP-4513", [], 50.0, 10.0) == "OP-4513 | sem medições"


def test_resumo_nao_altera_medicoes_nem_imprime(capsys):
    medicoes = [50.0, 60.0]
    ex.resumo_lote("OP-1", medicoes, 50.0, 10.0)
    assert medicoes == [50.0, 60.0]
    assert capsys.readouterr().out == "", "As funções devem devolver texto, não imprimir."
