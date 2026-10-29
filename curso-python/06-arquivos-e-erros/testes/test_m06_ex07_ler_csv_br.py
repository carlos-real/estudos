import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_ler_csv_br")

CONTEUDO = (
    "lote;linha;espessura;gramatura;observacao\r\n"
    "A-0153;A;25,4;23,10;COF: liberado\r\n"
    'A-0154; A ;;1.023,5;"Selagem; refazer"\r\n'
)


@pytest.fixture
def csv_excel(tmp_path):
    arquivo = tmp_path / "medicoes.csv"
    arquivo.write_bytes(CONTEUDO.encode("utf-8-sig"))
    return arquivo


def test_le_uma_linha_por_dicionario(csv_excel):
    linhas = ex.ler_csv_br(csv_excel, ["espessura", "gramatura"])
    assert len(linhas) == 2
    assert linhas[0] == {
        "lote": "A-0153",
        "linha": "A",
        "espessura": 25.4,
        "gramatura": 23.1,
        "observacao": "COF: liberado",
    }


def test_bom_nao_fica_no_nome_da_primeira_coluna(csv_excel):
    linhas = ex.ler_csv_br(csv_excel, [])
    assert "lote" in linhas[0], "Abra com encoding='utf-8-sig' para o BOM sumir."


def test_celula_numerica_vazia_vira_none(csv_excel):
    linhas = ex.ler_csv_br(csv_excel, ["espessura", "gramatura"])
    assert linhas[1]["espessura"] is None
    assert linhas[1]["gramatura"] == pytest.approx(1023.5)


def test_espacos_tirados_e_aspas_respeitadas(csv_excel):
    linhas = ex.ler_csv_br(csv_excel, ["espessura"])
    assert linhas[1]["linha"] == "A"
    assert linhas[1]["observacao"] == "Selagem; refazer", (
        "Use o módulo csv: ele entende o ';' dentro das aspas."
    )


def test_colunas_nao_numericas_continuam_texto(csv_excel):
    linhas = ex.ler_csv_br(csv_excel, ["espessura"])
    assert linhas[0]["gramatura"] == "23,10"


def test_nomes_de_coluna_com_espacos(tmp_path):
    arquivo = tmp_path / "espacos.csv"
    arquivo.write_bytes(" lote ; espessura \r\nB-1; 50,2 \r\n".encode("utf-8-sig"))
    assert ex.ler_csv_br(arquivo, ["espessura"]) == [{"lote": "B-1", "espessura": 50.2}]
