import copy

import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_revisao_tolerancias")

TOL = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
    },
    "B": {"espessura": {"nominal": 20.0, "tol_pct": 8.0}},
}


@pytest.mark.parametrize(
    ("nominal", "pct", "esperado"),
    [(50.0, 10.0, (45.0, 55.0)), (46.0, 5.0, (43.7, 48.3)), (20.0, 0.0, (20.0, 20.0))],
)
def test_limites(nominal, pct, esperado):
    assert ex.limites(nominal, pct) == esperado, "Lembre do round(..., 2) nos dois limites."


def test_amostra_sem_falhas():
    amostra = {"op": "OP-1", "linha": "A", "espessura": 50.1, "gramatura": 43.7}
    assert ex.falhas_da_amostra(amostra, TOL) == []


def test_falhas_na_ordem_das_propriedades():
    amostra = {"op": "OP-1", "linha": "A", "gramatura": 49.0, "espessura": 44.0}
    assert ex.falhas_da_amostra(amostra, TOL) == [
        "espessura 44.0 fora de 45.0 a 55.0",
        "gramatura 49.0 fora de 43.7 a 48.3",
    ]


def test_linha_normalizada_e_propriedade_ausente_ignorada():
    amostra = {"op": "OP-2", "linha": " b ", "espessura": 21.7, "gramatura": None}
    assert ex.falhas_da_amostra(amostra, TOL) == ["espessura 21.7 fora de 18.4 a 21.6"]


def test_linha_sem_tolerancia_devolve_none():
    assert ex.falhas_da_amostra({"op": "OP-3", "linha": "E", "espessura": 30.0}, TOL) is None


def test_textos_do_relatorio():
    aprovada = {"op": "OP-1", "linha": "a", "espessura": 50.0}
    reprovada = {"op": "OP-2", "linha": "A", "espessura": 56.3, "gramatura": 40.0}
    pendente = {"op": "OP-3", "linha": "E", "espessura": 30.0}
    assert ex.linha_do_relatorio(aprovada, TOL) == "OP-1 | linha A | APROVADA"
    assert ex.linha_do_relatorio(reprovada, TOL) == (
        "OP-2 | linha A | REPROVADA: espessura 56.3 fora de 45.0 a 55.0; "
        "gramatura 40.0 fora de 43.7 a 48.3"
    )
    assert ex.linha_do_relatorio(pendente, TOL) == (
        "OP-3 | linha E | PENDENTE: sem tolerância cadastrada"
    )


def test_relatorio_completo_com_total():
    amostras = [
        {"op": "OP-1", "linha": "A", "espessura": 50.0},
        {"op": "OP-2", "linha": "B", "espessura": 25.0},
        {"op": "OP-3", "linha": "E", "espessura": 30.0},
    ]
    assert ex.relatorio(amostras, TOL) == [
        "OP-1 | linha A | APROVADA",
        "OP-2 | linha B | REPROVADA: espessura 25.0 fora de 18.4 a 21.6",
        "OP-3 | linha E | PENDENTE: sem tolerância cadastrada",
        "Total: 3 amostras, 1 aprovadas (33.3%)",
    ]


def test_relatorio_sem_amostras():
    assert ex.relatorio([], TOL) == ["Total: 0 amostras, 0 aprovadas (0.0%)"]


def test_nao_altera_amostras_nem_tolerancias():
    amostras = [{"op": "OP-1", "linha": " a ", "espessura": 60.0}]
    copia_amostras = copy.deepcopy(amostras)
    copia_tol = copy.deepcopy(TOL)
    ex.relatorio(amostras, TOL)
    assert amostras == copia_amostras, "As amostras recebidas não podem ser alteradas."
    assert copia_tol == TOL
