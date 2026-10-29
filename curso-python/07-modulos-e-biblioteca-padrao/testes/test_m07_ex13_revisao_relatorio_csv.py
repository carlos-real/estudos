import json
from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_relatorio_csv")

CSV = """data;op;linha;ensaio;valor;resultado
06/10/2026;OP245103;C;espessura;44,5;reprovado
05/10/2026;OP245103;C;gramatura;35,1;aprovado
05/10/2026;OP245103;C;cof;0,25;Aprovado
01/10/2026;OP245101;A;espessura;20,4;aprovado
01/10/2026;OP245101;A;gramatura;1.018,8;aprovado
32/10/2026;OP245101;A;cof;0,21;aprovado
02/10/2026;OP245102;B;espessura;;aprovado
02/10/2026;OP245102;B;cof;0,33;REPROVADO
02/10/2026;OP245102;B;gramatura;19,9;reprovado
"""


@pytest.fixture
def arquivo(tmp_path):
    caminho = tmp_path / "ensaios.csv"
    caminho.write_text(CSV, encoding="utf-8")
    return caminho


def test_ler_conta_linhas_ignoradas(arquivo):
    registros, ignoradas = ex.ler_ensaios_csv(arquivo)
    assert len(registros) == 7
    assert ignoradas == 2, "Data 32/10 e valor vazio devem ser ignorados (e contados)"


def test_ler_converte_tipos(arquivo):
    registros, _ = ex.ler_ensaios_csv(arquivo)
    primeiro = registros[0]
    assert primeiro["data"] == date(2026, 10, 6)
    assert primeiro["op"] == "OP245103"
    assert primeiro["linha"] == "C"
    assert primeiro["ensaio"] == "espessura"
    assert primeiro["valor"] == pytest.approx(44.5)
    assert primeiro["resultado"] == "reprovado"


def test_ler_numero_com_milhar_e_resultado_minusculo(arquivo):
    registros, _ = ex.ler_ensaios_csv(arquivo)
    gramatura_a = [
        r for r in registros if r["op"] == "OP245101" and r["ensaio"] == "gramatura"
    ]
    assert gramatura_a[0]["valor"] == pytest.approx(1018.8)
    assert {r["resultado"] for r in registros} == {"aprovado", "reprovado"}


def test_resumo_por_op(arquivo):
    registros, _ = ex.ler_ensaios_csv(arquivo)
    assert ex.resumo_por_op(registros) == {
        "OP245101": {
            "linha": "A",
            "data": "01/10/2026",
            "ensaios": 2,
            "reprovados": [],
            "situacao": "aprovada",
        },
        "OP245102": {
            "linha": "B",
            "data": "02/10/2026",
            "ensaios": 2,
            "reprovados": ["cof", "gramatura"],
            "situacao": "reprovada",
        },
        "OP245103": {
            "linha": "C",
            "data": "05/10/2026",
            "ensaios": 3,
            "reprovados": ["espessura"],
            "situacao": "reprovada",
        },
    }


def test_resumo_ops_em_ordem_alfabetica(arquivo):
    registros, _ = ex.ler_ensaios_csv(arquivo)
    assert list(ex.resumo_por_op(registros)) == ["OP245101", "OP245102", "OP245103"]


def test_resumo_vazio():
    assert ex.resumo_por_op([]) == {}


def test_salvar_json_cria_pastas_e_preserva_acentos(tmp_path):
    destino = tmp_path / "saida" / "2026-10" / "situacao.json"
    dados = {"OP1": {"situacao": "reprovada", "observação": "COF acima"}}
    ex.salvar_json(dados, destino)
    texto = destino.read_text(encoding="utf-8")
    assert json.loads(texto) == dados
    assert "observação" in texto, "Use ensure_ascii=False para manter os acentos"
    assert "\n  " in texto, "Use indent=2 para o arquivo ficar legível"
